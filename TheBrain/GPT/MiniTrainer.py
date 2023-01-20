import os
from contextlib import nullcontext
import numpy as np
import torch
from TheBrain import Utils
from TheBrain.GPT import Faircoder
from Transformer_v2 import Fonfig, BigramLanguageModel, get_batch, estimate_loss
torch.manual_seed(1337)

print(torch.backends.mps.is_available())

import resource

os.environ["LRU_CACHE_CAPACITY"] = '1'
soft, hard = resource.getrlimit(resource.RLIMIT_AS)
resource.setrlimit(resource.RLIMIT_AS, (soft, hard))

out_dir = 'out2'

""" Setup Vocab Pickle """
meta = Utils.load_pickle_file(os.path.join(out_dir, 'meta.pkl'))
vocab_size = meta['vocab_size']
encode_meta = meta['encode']
decode_meta = meta['decode']
print(f"vocab_size = {vocab_size}")

""" Load Training Data """
t_data = np.memmap(os.path.join(out_dir, 'train.bin'), dtype=np.uint16, mode='r')
v_data = np.memmap(os.path.join(out_dir, 'val.bin'), dtype=np.uint16, mode='r')
# np.
# torch.tensor(t_data)
train_data = torch.tensor(t_data, dtype=torch.long)
val_data = torch.tensor(v_data, dtype=torch.long)

""" Create Config for Transformer """
config = Fonfig()
config.vocab_size = vocab_size
config.train_data = train_data
config.val_data = val_data

dtype = 'bfloat16' # 'float32' or 'bfloat16'
ptdtype = {'float32': torch.float32, 'bfloat16': torch.bfloat16}[dtype]
# ctx = nullcontext() if config.device_type == 'mps' else torch.amp.autocast(device_type=config.device_type, dtype=ptdtype)
# torch.amp.autocast(device_type=config.device_type, dtype=ptdtype)
""" Help Clear Some Memory """
t_data = None
v_data = None
train_data = None
val_data = None
# meta = None

""" Initialize Transformer Model """
model = BigramLanguageModel(config=config)
m = model.to(config.device)
print(sum(p.numel() for p in m.parameters())/1e6, 'M parameters')

# create a PyTorch optimizer
optimizer = torch.optim.AdamW(m.parameters(), lr=config.learning_rate)
print(" BEGIN TRAINING LOOP! ")
for iter in range(config.max_iters):
    print("Training Round:", iter)
    # every once in a while evaluate the loss on train and val sets
    if iter % config.eval_interval == 0 or iter == config.max_iters - 1:
        losses = estimate_loss(m, config)
        print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")
        if losses['val'] < config.best_val_loss or config.always_save_checkpoint:
            best_val_loss = losses['val']
            raw_model = m
            if config.iter_num % config.eval_interval == 0 and config.always_save_checkpoint:
                checkpoint = {
                    'model': raw_model.state_dict(),
                    'optimizer': optimizer.state_dict(),
                    'model_args': config,
                    'iter_num': config.iter_num,
                    'best_val_loss': best_val_loss
                }
                print(f"saving checkpoint to {out_dir}")
                torch.save(checkpoint, os.path.join(out_dir, 'ckpt.pt'))

    # sample a batch of data
    xb, yb = get_batch('train', config)
    # evaluate the loss
    logits, loss = m(xb, yb)
    del xb, yb
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    del logits, loss
    optimizer.step()


# meta = Utils.load_pickle_file(os.path.join(out_dir, 'meta.pkl'))
decoder = Faircoder.get_decoder_object(decode_meta)
# generate from the model
context = torch.zeros((1, 1), dtype=torch.long, device=config.device)
raw_output = m.generate(context, max_new_tokens=500)[0].tolist()
decoded = decoder(raw_output)
print(decoded)
#open('more.txt', 'w').write(decode(m.generate(context, max_new_tokens=10000)[0].tolist()))
