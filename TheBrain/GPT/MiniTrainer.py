import os

import numpy as np
import torch

from TheBrain import Utils
from Transformer_v2 import Fonfig, BigramLanguageModel, estimate_loss, get_batch
out_dir = 'out2'
# poor man's data loader, TODO evaluate need for actual DataLoader
t_data = np.memmap(os.path.join(out_dir, 'train.bin'), dtype=np.uint16, mode='r')
v_data = np.memmap(os.path.join(out_dir, 'val.bin'), dtype=np.uint16, mode='r')

meta = Utils.load_pickle_file(os.path.join(out_dir, 'meta.pkl'))
vocab_size = meta['vocab_size']
print(f"vocab_size = {vocab_size}")


# train_data = torch.tensor(t_data, dtype=torch.long)
# val_data = torch.tensor(v_data, dtype=torch.long)

config = Fonfig()
config.vocab_size = vocab_size
config.train_data = t_data
config.val_data = v_data

model = BigramLanguageModel(config=config)
m = model.to(config.device)
# print the number of parameters in the model
print(sum(p.numel() for p in m.parameters())/1e6, 'M parameters')

# create a PyTorch optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)

for iter in range(config.max_iters):

    # every once in a while evaluate the loss on train and val sets
    if iter % config.eval_interval == 0 or iter == config.max_iters - 1:
        losses = estimate_loss(model, config)
        print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")

    # sample a batch of data
    xb, yb = get_batch('train', config)

    # evaluate the loss
    logits, loss = model(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()