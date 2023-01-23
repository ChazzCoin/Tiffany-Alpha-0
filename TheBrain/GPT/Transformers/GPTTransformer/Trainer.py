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
import torch
from F import OS
from GPTTransformer import GPTConfig, GPT
from TheBrain.GPT.DataVocabGenerators import DataSetGenerator
from TheBrain.GPT.Encoders import TikToken
from TheBrain.GPT.Transformers.FonFig import FonfigGPT, CHECKPOINT_GPT
from TheBrain.GPT import out as o
from TheBrain import Utils

DATA_LOAD = { "train_data": "", "val_data": "" }

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
    DATA_LOAD["train_data"] = _tensor_data[:_n]
    DATA_LOAD["val_data"] = _tensor_data[_n:]
    if saveTrainValData:
        print("Saving New Training and Validation Data. ")
        torch.save(DATA_LOAD["train_data"], o.OUT_FILE_GETTER(o._training_name))
        torch.save(DATA_LOAD["val_data"], o.OUT_FILE_GETTER(o._val_name))
    return _vocab_size

def setup_checkpoint_dataset():
    DATA_LOAD["train_data"] = TORCH_LOADER(o.OUT_FILE_GETTER(o._training_name))
    DATA_LOAD["val_data"] = TORCH_LOADER(o.OUT_FILE_GETTER(o._val_name))


""" model init -> Scratch, Resume """
iteration_count = 0
if checkpoint and config.init_from == 'resume':
    print(f"Resuming Training from Checkpoint.")

    if config.load_from_checkpoint_dataset:
        print("Loading Existing Training and Validation Data. ")
        setup_checkpoint_dataset()
    else:
        print("Loading New Training and Validation Data. ")
        setup_new_dataset(articleLimit=100000)

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
    v_size = setup_new_dataset()
    """ Setup Config """
    config.vocab_size = v_size
    config.train_data_path = o.OUT_FILE_GETTER(o._training_name)
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

""" Training Loop """
t0 = time.time()
# init these up here, can override if init_from='resume' (i.e. from a checkpoint)
best_val_loss = 1e9
save_counter = 0
while True:

    # determine the learning rate for this iteration
    if config.decay_lr:
        lr = Utils.get_lr(iteration_count, config)
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr
    else:
        lr = config.learning_rate

    # evaluate the loss on train/val sets and write checkpoints
    if iteration_count % config.eval_interval == 0:
        losses = Utils.estimate_loss(model, config, DATA_LOAD["train_data"], DATA_LOAD["val_data"])
        print(f"Round: [ {iteration_count} ] Train -> LOSS: [ {losses['train']:.4f} ]")
        print(f"Round: [ {iteration_count} ] Val -> LOSS: [ {losses['val']:.4f} ]")
        if losses['val'] < best_val_loss or config.always_save_checkpoint:
            best_val_loss = losses['val']
            raw_model = model.module if config.ddp else model
            if iteration_count % config.save_count_interval == 0:
                """ Saving Checkpoint. """
                checkpoint = CHECKPOINT_GPT(raw_model.state_dict(),
                                            optimizer.state_dict(),
                                            model_args, iteration_count+1,
                                            best_val_loss, config)
                checkpoint_path = o.OUT_FILE_GETTER(config.checkpoint_file_name)
                TORCH_SAVER(checkpoint, checkpoint_path)
                print(f"Saved Checkpoint to: [ {checkpoint_path} ]")
    if iteration_count == 0 and config.eval_only:
        break

    # forward backward update, with optional gradient accumulation to simulate larger batch size
    optimizer.zero_grad(set_to_none=True)
    for micro_step in range(config.gradient_accumulation_steps):
        X, Y = Utils.get_batch('train', config, DATA_LOAD["train_data"], DATA_LOAD["val_data"])
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
        print(f"Round: [ {iteration_count} ] LOSS: [ {lossf:.4f} ], TIME: [ {dt*1000:.2f}ms ]")
    iteration_count += 1

    # termination conditions
    if iteration_count > config.max_iters:
        break
