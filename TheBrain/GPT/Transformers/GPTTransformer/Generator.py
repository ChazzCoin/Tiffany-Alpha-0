"""
Sample from a trained model
"""
import os
from TheBrain import Utils
from contextlib import nullcontext
import torch
from F import OS

from TheBrain.GPT.Encoders import Faircoder
from GPTTransformer import GPTConfig, GPT

# -----------------------------------------------------------------------------
cwd = OS.get_cwd()
out_dir = '../../out'
start = "\n" # or "<|endoftext|>" or whatever you like
num_samples = 10 # number of samples to draw
max_new_tokens = 500 # number of tokens generated in each sample
temperature = 0.8 # higher temperature (up to 1) is more random, lower (down to 0) means more greedy
top_k = 200 # retain only the top_k most likely tokens, clamp others to have 0 probability
seed = 1337
device = 'cpu' # examples: 'cpu', 'cuda', 'cuda:0', 'cuda:1', etc.
dtype = 'bfloat16' # 'float32' or 'bfloat16' or 'float16'
exec(open('../../configurator.py').read()) # overrides from command line or config file
# -----------------------------------------------------------------------------

torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.backends.cuda.matmul.allow_tf32 = True # allow tf32 on matmul
torch.backends.cudnn.allow_tf32 = True # allow tf32 on cudnn
device_type = 'cpu' if 'cuda' in device else 'cpu' # for later use in torch.autocast
ptdtype = {'float32': torch.float32, 'bfloat16': torch.bfloat16, 'float16': torch.float16}[dtype]
ctx = nullcontext() if device_type == 'cpu' else torch.amp.autocast(device_type=device_type, dtype=ptdtype)

# model
ckpt_path = os.path.join(out_dir, 'ckpt.pt')
checkpoint = torch.load(ckpt_path, map_location=device)

gptconf = GPTConfig(**checkpoint['model_args'])
model = GPT(gptconf)

state_dict = checkpoint['model']
unwanted_prefix = '_orig_mod.'
for k,v in list(state_dict.items()):
    if k.startswith(unwanted_prefix):
        state_dict[k[len(unwanted_prefix):]] = state_dict.pop(k)

model.load_state_dict(state_dict)
model.eval()
model.to(device)

""" LOAD META VOCAB FILE """
print(f"Loading meta...")
meta = Utils.load_pickle_file(f'{cwd}/out/meta.pkl')
# TODO want to make this more general to arbitrary encoder/decoder schemes
e, d = meta['encode'], meta['decode']
encode = Faircoder.get_encoder_object(e)
decode = Faircoder.get_decoder_object(d)

# encode the beginning of the prompt
start_ids = encode(start)
x = (torch.tensor(start_ids, dtype=torch.long, device=device)[None, ...])

# run generation
with torch.no_grad():
    with ctx:
        for k in range(num_samples):
            y = model.generate(x, max_new_tokens, temperature=temperature, top_k=top_k)
            print(decode(y[0].tolist()))
            print('---------------')