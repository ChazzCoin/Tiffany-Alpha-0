import math
import pickle
import torch


def get_batch(split, config, train_data, val_data):
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - config.block_size, (config.batch_size,))
    x = torch.stack([data[i:i+config.block_size] for i in ix])
    y = torch.stack([data[i+1:i+config.block_size+1] for i in ix])
    x, y = x.to(config.device), y.to(config.device)
    return x, y

# todo: move this into Utils.
@torch.no_grad()
def estimate_loss(model, config, train_data, val_data):
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(config.eval_iters)
        for k in range(config.eval_iters):
            X, Y = get_batch(split, config, train_data, val_data)
            # with ctx:
            logits, loss = model(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out


"""# learning rate decay scheduler (cosine with warmup)"""
def get_lr(iter_num, config):
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

def load_pickle_file(picklePath):
    with open(picklePath, 'rb') as f:
        pkl = pickle.load(f)
    return pkl

def save_pickle_file(picklePath, pickleFile):
    with open(picklePath, 'wb') as f:
        pickle.dump(pickleFile, f)