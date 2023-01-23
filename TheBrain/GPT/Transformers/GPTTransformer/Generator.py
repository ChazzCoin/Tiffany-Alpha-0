"""
Sample from a trained model
"""
import torch
from TheBrain.GPT.Encoders import TikToken
from GPTTransformer import GPTConfig, GPT

start = "tell me a story" # or "<|endoftext|>" or whatever you like
num_samples = 10 # number of samples to draw
max_new_tokens = 500 # number of tokens generated in each sample
temperature = 0.8 # higher temperature (up to 1) is more random, lower (down to 0) means more greedy
top_k = 200 # retain only the top_k most likely tokens, clamp others to have 0 probability


from TheBrain.GPT import out as o
TORCH_LOADER = lambda file_path: torch.load(file_path)
# model
checkpoint = TORCH_LOADER(o.OUT_FILE_GETTER(o._checkpoint_name))
config = checkpoint['fonfigGPT']
state_dict = checkpoint['model']
model_args = checkpoint['model_args']

gptconf = GPTConfig(**model_args)
model = GPT(gptconf)
model.load_state_dict(state_dict)
model.eval()
model.to(config.device)

""" LOAD META VOCAB FILE """
print(f"Loading Encoder and Decoder...")
start_ids = TikToken.encode(start)
x = (torch.tensor(start_ids, dtype=torch.long, device=config.device)[None, ...])

# run generation
with torch.no_grad():
    for k in range(num_samples):
        y = model.generate(x, max_new_tokens, temperature=temperature, top_k=top_k)
        print(TikToken.decode(y[0].tolist()))
        print('---------------')