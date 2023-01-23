import torch
from TheBrain import Utils


""" 1. Input: All Text -> Extracts Unique Characters -> Output: List[Char] """
CREATE_VOCAB = lambda text: sorted(list(set(text)))

""" Input: List[Char] -> Encoder Mapping. -> Output: Dict{ Int: Char }
Key = Character
Value = Int
"""
ENCODE_TO_DICT = lambda vocab: {ch: i for i, ch in enumerate(vocab)}
FAIR_ENCODER = lambda s, encoder_dict: [encoder_dict[c] for c in s]

""" Input: List[Char] -> Decoder Mapping. -> Output: Dict{ Int: Char } 
Key = Int
Value = Character
"""
DECODE_TO_DICT = lambda vocab: {i: ch for i, ch in enumerate(vocab)}
FAIR_DECODER = lambda l, decoder_dict: ''.join([decoder_dict[i] for i in l])

TO_TENSOR = lambda data: torch.tensor(data, dtype=torch.long)
SPLIT_90_PERCENT = lambda data: data[:int(0.9 * len(data))]
SPLIT_10_PERCENT = lambda data: data[int(0.9 * len(data)):]
SPLIT_TRAINING_VAL = lambda data: (SPLIT_90_PERCENT(data), SPLIT_10_PERCENT(data))

def get_encoder_object(encoder_dict):
    return lambda s: [encoder_dict[str(c)] for c in s]

def get_decoder_object(decoder_dict):
    return lambda l: ''.join([decoder_dict[i] for i in l])

def get_vocab_pickle(metaPath):
    return Utils.load_pickle_file(metaPath)

def encoder_from_pickle(meta):
    e, _ = meta['encode'], meta['decode']
    return get_encoder_object(e)

def decoder_from_pickle(meta):
    _, d = meta['encode'], meta['decode']
    return get_decoder_object(d)

def encoder_from_vocab(metaPath):
    meta = get_vocab_pickle(metaPath)
    e, _ = meta['encode'], meta['decode']
    return get_encoder_object(e)

def decoder_from_vocab(metaPath):
    meta = get_vocab_pickle(metaPath)
    _, d = meta['encode'], meta['decode']
    return get_decoder_object(d)

def get_encode_decode_dictionaries(data) -> (dict,dict):
    vocab = CREATE_VOCAB(data)
    edict = ENCODE_TO_DICT(vocab)
    dedict = DECODE_TO_DICT(vocab)
    return edict, dedict
