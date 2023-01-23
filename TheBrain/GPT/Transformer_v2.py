import numpy as np
import torch
import torch.nn as nn
from torch.nn import functional as F
import gc
class Fonfig:
    # hyperparameters
    init_from = 'resume'
    always_save_checkpoint = False
    save_iters = 10
    vocab_size = 0
    train_data = None
    val_data = None
    iter_num = 200
    max_iters = 200
    eval_iters = 1
    eval_interval = 5
    best_val_loss = 1e9
    batch_size = 32 # how many independent sequences will we process in parallel?
    block_size = 64 # what is the maximum context length for predictions?
    learning_rate = 3e-4
    device_type = 'cpu'
    device = 'cpu'
    # Hardware Performance Settings
    n_embd = 16
    n_head = 8
    n_layer = 8
    dropout = 0.2
    # ------------

# torch.manual_seed(1337)

# # # data loading
# def get_batch(split, config:Fonfig):
#     # generate a small batch of data of inputs x and targets y
#     # gc.collect()
#     data = config.train_data if split == 'train' else config.val_data
#     ix = torch.randint(len(data) - config.block_size, (config.batch_size,))
#     x = torch.stack([data[i:i+config.block_size] for i in ix])
#     y = torch.stack([data[i+1:i+config.block_size+1] for i in ix])
#     x, y = x.to(config.device), y.to(config.device)
#     return x, y
#
#
# def get_batch2(split, config:Fonfig):
#     gc.collect()
#     data = config.train_data if split == 'train' else config.val_data
#     ix = torch.randint(len(data) - config.block_size, (config.batch_size,))
#     x = torch.stack([torch.from_numpy((data[i:i+config.block_size]).astype(np.int64)) for i in ix])
#     y = torch.stack([torch.from_numpy((data[i+1:i+1+config.block_size]).astype(np.int64)) for i in ix])
#     x, y = x.to(config.device), y.to(config.device)
#     return x, y
# @torch.no_grad()
# def estimate_loss(model, config:Fonfig):
#     out = {}
#     model.eval()
#     for split in ['train', 'val']:
#         losses = torch.zeros(config.eval_iters)
#         for k in range(config.eval_iters):
#             X, Y = get_batch(split, config)
#             logits, loss = model(X, Y)
#             # del X, Y, logits
#             losses[k] = loss.item()
#             # del loss
#             # gc.collect()
#         out[split] = losses.mean()
#     model.train()
#     return out

class Head(nn.Module):
    """ one head of self-attention """

    def __init__(self, head_size, config:Fonfig):
        super().__init__()
        self.key = nn.Linear(config.n_embd, head_size, bias=False)
        self.query = nn.Linear(config.n_embd, head_size, bias=False)
        self.value = nn.Linear(config.n_embd, head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(config.block_size, config.block_size)))

        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x):
        B,T,C = x.shape
        k = self.key(x)   # (B,T,C)
        q = self.query(x) # (B,T,C)
        # compute attention scores ("affinities")
        wei = q @ k.transpose(-2,-1) * C**-0.5 # (B, T, C) @ (B, C, T) -> (B, T, T)
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf')) # (B, T, T)
        wei = F.softmax(wei, dim=-1) # (B, T, T)
        wei = self.dropout(wei)
        # perform the weighted aggregation of the values
        v = self.value(x) # (B,T,C)
        out = wei @ v # (B, T, T) @ (B, T, C) -> (B, T, C)
        return out

class MultiHeadAttention(nn.Module):
    """ multiple heads of self-attention in parallel """

    def __init__(self, head_size, config:Fonfig):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size, config) for _ in range(config.n_head)])
        self.proj = nn.Linear(config.n_embd, config.n_embd)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.dropout(self.proj(out))
        return out

class FeedFoward(nn.Module):
    """ a simple linear layer followed by a non-linearity """

    def __init__(self, config:Fonfig):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(config.n_embd, 4 * config.n_embd),
            nn.ReLU(),
            nn.Linear(4 * config.n_embd, config.n_embd),
            nn.Dropout(config.dropout),
        )

    def forward(self, x):
        return self.net(x)

class Block(nn.Module):
    """ Transformer block: communication followed by computation """

    def __init__(self, config:Fonfig):
        # n_embd: embedding dimension, n_head: the number of heads we'd like
        super().__init__()
        head_size = config.n_embd // config.n_head
        self.sa = MultiHeadAttention(head_size, config)
        self.ffwd = FeedFoward(config)
        self.ln1 = nn.LayerNorm(config.n_embd)
        self.ln2 = nn.LayerNorm(config.n_embd)

    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x

# super simple bigram model
class BigramLanguageModel(nn.Module):
    _config = None

    def __init__(self, config:Fonfig=None):
        super().__init__()
        # each token directly reads off the logits for the next token from a lookup table
        self._config = config
        self.token_embedding_table = nn.Embedding(self._config.vocab_size, self._config.n_embd)
        self.position_embedding_table = nn.Embedding(self._config.block_size, self._config.n_embd)
        self.blocks = nn.Sequential(*[Block(self._config) for _ in range(self._config.n_layer)])
        self.ln_f = nn.LayerNorm(self._config.n_embd) # final layer norm
        self.lm_head = nn.Linear(self._config.n_embd, self._config.vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        # idx and targets are both (B,T) tensor of integers
        tok_emb = self.token_embedding_table(idx) # (B,T,C)
        pos_emb = self.position_embedding_table(torch.arange(T, device=self._config.device)) # (T,C)
        x = tok_emb + pos_emb # (B,T,C)
        x = self.blocks(x) # (B,T,C)
        x = self.ln_f(x) # (B,T,C)
        logits = self.lm_head(x) # (B,T,vocab_size)

        if targets is None:
            loss = None
        else:
            B, T, C = logits.shape
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets)

        return logits, loss

    def generate(self, idx, max_new_tokens):
        # idx is (B, T) array of indices in the current context
        for _ in range(max_new_tokens):
            # crop idx to the last block_size tokens
            idx_cond = idx[:, -self._config.block_size:]
            # get the predictions
            logits, loss = self(idx_cond)
            # focus only on the last time step
            logits = logits[:, -1, :] # becomes (B, C)
            # apply softmax to get probabilities
            probs = F.softmax(logits, dim=-1) # (B, C)
            # sample from the distribution
            idx_next = torch.multinomial(probs, num_samples=1) # (B, 1)
            # append sampled index to the running sequence
            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)
        return idx

