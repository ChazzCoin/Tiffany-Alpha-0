import os

from F import OS
import torch
from TheBrain.GPT.DataVocabGenerators import DataSetGenerator
from TheBrain.GPT.Encoders import TikToken
from TheBrain.GPT.BiGramTransformer.Transformer_v2 import Fonfig, BigramLanguageModel

import resource
os.environ["LRU_CACHE_CAPACITY"] = '1'
soft, hard = resource.getrlimit(resource.RLIMIT_AS)
resource.setrlimit(resource.RLIMIT_AS, (soft, hard))
cwd = OS.get_cwd()
out_dir = 'out2'


""" DATA SET """
text = DataSetGenerator.get_raw_data_set(articleLimit=10000)

""" Fair ENCODER """
# encoder_dict = VocabGenerators.load_fair_encoder()
# ENCODE = Faircoder.get_encoder_object(encoder_dict)
# decoder_dict = VocabGenerators.load_fair_decoder()
# DECODE = Faircoder.get_decoder_object(decoder_dict)
# encoded_data = ENCODE(text)
# vocab_size = len(encoded_data)

""" TIKTOKEN ENCODER """
encoded_data = TikToken.encode(text)
vocab_size = TikToken.get_tiktoken_vocab_count()


""" RAW ENCODER """
# chars = sorted(list(set(text)))
# vocab_size = len(chars)
# # create a mapping from characters to integers
# stoi = { ch:i for i,ch in enumerate(chars) }
# itos = { i:ch for i,ch in enumerate(chars) }
# ENCODE = lambda s: [stoi[c] for c in s] # encoder: take a string, output a list of integers
# DECODE = lambda l: ''.join([itos[i] for i in l]) # decoder: take a list of integers, output a string
# encoded_data = ENCODE(text)

""" Setup Train/Val Data """
data = torch.tensor(encoded_data, dtype=torch.long)
n = int(0.9*len(data)) # first 90% will be train, rest val
train_data = data[:n]
val_data = data[n:]


print(f"vocab_size = {vocab_size}")
""" Load Training Data """

""" Create Config for Transformer """
config = Fonfig()
config.vocab_size = vocab_size
config.train_data = train_data
config.val_data = val_data

""" Help Clear Some Memory """
del train_data, val_data

""" Initialize Transformer Model """
model = BigramLanguageModel(config=config)
m = model.to(config.device)
print(sum(p.numel() for p in m.parameters())/1e6, 'M parameters')

def get_batch(split):
    # generate a small batch of data of inputs x and targets y
    # gc.collect()
    data = config.train_data if split == 'train' else config.val_data
    ix = torch.randint(len(data) - config.block_size, (config.batch_size,))
    x = torch.stack([data[i:i+config.block_size] for i in ix])
    y = torch.stack([data[i+1:i+config.block_size+1] for i in ix])
    x, y = x.to(config.device), y.to(config.device)
    return x, y

@torch.no_grad()
def estimate_loss():
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(config.eval_iters)
        for k in range(config.eval_iters):
            X, Y = get_batch(split)
            logits, loss = model(X, Y)
            # del X, Y, logits
            losses[k] = loss.item()
            # del loss
            # gc.collect()
        out[split] = losses.mean()
    model.train()
    return out

# create a PyTorch optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
print(" BEGIN TRAINING LOOP! ")
for iter in range(config.max_iters):
    print(iter)
    # every once in a while evaluate the loss on train and val sets
    if iter % config.eval_interval == 0 or iter == config.max_iters - 1:
        losses = estimate_loss()
        print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")

    # sample a batch of data
    xb, yb = get_batch('train')

    # evaluate the loss
    logits, loss = model(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()


# meta = Utils.load_pickle_file(os.path.join(out_dir, 'meta.pkl'))

# generate from the model
context = torch.zeros((1, 1), dtype=torch.long, device=config.device)
encoded_output = model.generate(context, max_new_tokens=500)[0].tolist()
print(encoded_output)
decoded = TikToken.decode(encoded_output)
# decoded = DECODE(encoded_output)
print(decoded)
#open('more.txt', 'w').write(decode(m.generate(context, max_new_tokens=10000)[0].tolist()))
