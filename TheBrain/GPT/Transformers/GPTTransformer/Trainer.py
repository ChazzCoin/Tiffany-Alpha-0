"""
This training script can be run both on a single gpu in debug mode,
and also in a larger training run with distributed data parallel (ddp).
To run on a single GPU, example:
$ python train.py --batch_size=32 --compile=False
To run with DDP on 4 gpus on 1 node, example:
$ torchrun --standalone --nproc_per_node=4 train.py
To run with DDP on 4 gpus across 2 nodes, example:
- Run on the first (master) node with example IP 123.456.123.456:
$ torchrun --nproc_per_node=8 --nnodes=2 --node_rank=0 --master_addr=123.456.123.456 --master_port=1234 train.py
- Run on the worker node:
$ torchrun --nproc_per_node=8 --nnodes=2 --node_rank=1 --master_addr=123.456.123.456 --master_port=1234 train.py
(If your cluster does not have Infiniband interconnect prepend NCCL_IB_DISABLE=1)
"""

import time
import math
import torch
from F import OS
from GPTTransformer import GPTConfig, GPT
from TheBrain.GPT.DataVocabGenerators import DataSetGenerator
from TheBrain.GPT.Encoders import TikToken
from TheBrain.GPT.Transformers.FonFig import FonfigGPT, CHECKPOINT_GPT
from TheBrain.GPT import out as o

TORCH_LOADER = lambda file_path: torch.load(file_path)
TORCH_SAVER = lambda data, file_path: torch.save(data, file_path)

cwd = OS.get_cwd()
out_dir = o.OUT_PATH
config = FonfigGPT()
checkpoint = None

try:
    checkpoint = TORCH_LOADER(o.OUT_FILE_GETTER(o._checkpoint_name))
    config = checkpoint['fonfigGPT']
    print("Checkpoint Loaded!")
except:
    print("No Checkpoint.")


def setup_new_dataset(articleLimit=1000, saveTrainValData=True):
    """ DATA SET """
    _text = DataSetGenerator.get_raw_data_set(articleLimit=articleLimit)
    """ TIKTOKEN ENCODER """
    _encoded_data = TikToken.encode(_text)
    _vocab_size = TikToken.get_tiktoken_vocab_count()
    """ Setup Train/Val Data """
    _tensor_data = torch.tensor(_encoded_data, dtype=torch.long)
    _n = int(0.9 * len(_tensor_data))  # first 90% will be train, rest val
    _train_data = _tensor_data[:_n]
    _val_data = _tensor_data[_n:]
    if saveTrainValData:
        torch.save(train_data, o.OUT_FILE_GETTER(o._training_name))
        torch.save(val_data, o.OUT_FILE_GETTER(o._val_name))
    return _vocab_size, _train_data, _val_data


""" model init -> Scratch, Resume """
iteration_count = 0
if checkpoint and config.init_from == 'resume':
    print(f"Resuming Training from Checkpoint.")
    train_data = TORCH_LOADER(o.OUT_FILE_GETTER(o._training_name))
    val_data = TORCH_LOADER(o.OUT_FILE_GETTER(o._val_name))
    model_args = checkpoint['model_args']
    state_dict = checkpoint['model']
    iteration_count = checkpoint['iteration_count']
    best_val_loss = checkpoint['best_val_loss']
    optimizer_state_dict = checkpoint['optimizer']
    config.max_iters += config.max_iters
    config.lr_decay_iters += config.lr_decay_iters
    # Initialize Model with checkpoint Model Args and State Dict.
    gptconf = GPTConfig(**model_args)
    model = GPT(gptconf)
    model.load_state_dict(state_dict)
    model.to(config.device)

else:
    # init a new model from scratch
    print("Initializing a New Model from scratch")
    """ Setup New DataSet """
    v_size, t_data, v_data = setup_new_dataset()
    """ Setup Config """
    config.vocab_size = v_size
    config.train_data = t_data
    config.train_data_path = o.OUT_FILE_GETTER(o._training_name)
    config.val_data = v_data
    config.val_data_path = o.OUT_FILE_GETTER(o._val_name)

    """ Setup Model Args """
    model_args = dict(n_layer=config.n_layer,
                      n_head=config.n_head,
                      n_embd=config.n_embd,
                      block_size=config.block_size,
                      dropout=config.dropout,
                      vocab_size=config.vocab_size)

    gptconf = GPTConfig(**model_args)
    model = GPT(gptconf)
    model.to(config.device)
    iteration_count = 0



# crop down the model block size if desired
if config.block_size < model.config.block_size:
    model.crop_block_size(config.block_size)


# optimizer
optimizer = model.configure_optimizers(config.weight_decay, config.learning_rate, (config.beta1, config.beta2))
if checkpoint or config.init_from == 'resume':
    optimizer.load_state_dict(checkpoint['optimizer'])

def get_batch(split):
    data = config.train_data if split == 'train' else config.val_data
    ix = torch.randint(len(data) - config.block_size, (config.batch_size,))
    x = torch.stack([data[i:i+config.block_size] for i in ix])
    y = torch.stack([data[i+1:i+config.block_size+1] for i in ix])
    x, y = x.to(config.device), y.to(config.device)
    return x, y

# todo: move this into Utils.
@torch.no_grad()
def estimate_loss():
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(config.eval_iters)
        for k in range(config.eval_iters):
            X, Y = get_batch(split)
            # with ctx:
            logits, loss = model(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out

"""# learning rate decay scheduler (cosine with warmup)"""
def get_lr(iter_num):
    # 1) linear warmup for warmup_iters steps
    if iter_num < config.warmup_iters:
        return config.learning_rate * iter_num / config.warmup_iters
    # 2) if iter > lr_decay_iters, return min learning rate
    if iter_num > config.lr_decay_iters:
        return config.min_lr
    # 3) in between, use cosine decay down to min learning rate
    decay_ratio = (iter_num - config.warmup_iters) / (config.lr_decay_iters - config.warmup_iters)
    assert 0 <= decay_ratio <= 1
    coeff = 0.5 * (1.0 + math.cos(math.pi * decay_ratio)) # coeff ranges 0..1
    return config.min_lr + coeff * (config.learning_rate - config.min_lr)


""" Training Loop """
t0 = time.time()
# init these up here, can override if init_from='resume' (i.e. from a checkpoint)
best_val_loss = 1e9
save_counter = 0
while True:

    # determine the learning rate for this iteration
    if config.decay_lr:
        lr = get_lr(iteration_count)
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr
    else:
        lr = config.learning_rate

    # evaluate the loss on train/val sets and write checkpoints
    if iteration_count % config.eval_interval == 0:
        losses = estimate_loss()
        print(f"step {iteration_count}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")
        if losses['val'] < best_val_loss or config.always_save_checkpoint:
            best_val_loss = losses['val']
            raw_model = model.module if config.ddp else model
            if iteration_count % config.save_count_interval == 0:
                """ Saving Checkpoint. """
                checkpoint = CHECKPOINT_GPT(raw_model.state_dict(),
                                            optimizer.state_dict(),
                                            model_args, iteration_count,
                                            best_val_loss, config)
                checkpoint_path = o.OUT_FILE_GETTER(config.checkpoint_file_name)
                TORCH_SAVER(checkpoint, checkpoint_path)
                print(f"Saved Checkpoint to: [ {checkpoint_path} ]")
    if iteration_count == 0 and config.eval_only:
        break

    # forward backward update, with optional gradient accumulation to simulate larger batch size
    optimizer.zero_grad(set_to_none=True)
    for micro_step in range(config.gradient_accumulation_steps):
        X, Y = get_batch('train')
        if config.ddp:
            # in DDP training we only need to sync gradients at the last micro step.
            # the official way to do this is with model.no_sync() context manager, but
            # I really dislike that this bloats the code and forces us to repeat code
            # looking at the source of that context manager, it just toggles this variable
            model.require_backward_grad_sync = (micro_step == config.gradient_accumulation_steps - 1)
        # with ctx:
        logits, loss = model(X, Y)
        loss.backward()
    optimizer.step()

    # timing and logging
    t1 = time.time()
    dt = t1 - t0
    t0 = t1
    if iteration_count % config.log_interval == 0:
        lossf = loss.item() # loss as float. TODO note CPU-GPU sync! profile, make sure not too slow
        print(f"iter {iteration_count}: loss {lossf:.4f}, time {dt*1000:.2f}ms")
    iteration_count += 1

    # termination conditions
    if iteration_count > config.max_iters:
        break
