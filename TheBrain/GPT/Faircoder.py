import torch
from TheBrain import Utils

""" 1. Input: All Text -> Extracts Unique Characters -> Output: List[Char] """
extract_vocab = lambda text: sorted(list(set(text)))

""" Input: List[Char] -> Encoder Mapping. -> Output: Dict{ Int: Char }
Key = Character
Value = Int
"""
encoder_dictionary = lambda vocab: {ch: i for i, ch in enumerate(vocab)}
encoder = lambda s, encoder_dict: [encoder_dict[c] for c in s]

""" Input: List[Char] -> Decoder Mapping. -> Output: Dict{ Int: Char } 
Key = Int
Value = Character
"""
decoder_dictionary = lambda vocab: {i: ch for i, ch in enumerate(vocab)}
decoder = lambda l, decoder_dict: ''.join([decoder_dict[i] for i in l])

encoded_data = lambda encodedText: torch.tensor(encodedText, dtype=torch.long)
training_data = lambda data: data[:int(0.9 * len(data))]
val_data = lambda data: data[int(0.9 * len(data)):]
training_val_data = lambda data: (training_data(data), val_data(data))

def get_encoder_object(encoder_dict):
    return lambda s: [encoder_dict[c] for c in s]

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
    vocab = extract_vocab(data)
    edict = encoder_dictionary(vocab)
    dedict = decoder_dictionary(vocab)
    return edict, dedict
