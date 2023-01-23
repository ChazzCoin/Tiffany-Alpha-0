import pickle
import numpy as np

from TheBrain.GPT.Encoders import Faircoder as fc, Faircoder
from TheBrain.BrainDB.ArticleProvider import Provider
from F import OS, FILE

cwd = FILE.get_file_path(__file__=__file__)
def get_data_set(articleLimit=1000):
    _DATA = ""
    # Shakespeare
    with open(f'{cwd}/input.txt', 'r') as f:
        _DATA += f.read()

    """ GET ARTICLES """
    db = Provider()
    result = db.get_articles(limit=articleLimit)
    print("Article Count:", len(result))
    for art in result:
        temp_all = str(art)
        _DATA += temp_all
    return _DATA

OUT_DIR = "/out2"
CREATE_TRAINING_DATA_SET = True

""" Create Vocab """
DATA = get_data_set()
DATA_en = str(DATA).encode('utf8')
DATA_de = DATA_en.decode()
vocab_size = len(DATA)
print("Vocab Size:", vocab_size)
RAW_vocab = fc.CREATE_VOCAB(DATA)
print("Unique Character Count:", len(RAW_vocab))
ENCODER_dict = fc.ENCODE_TO_DICT(RAW_vocab)
print(ENCODER_dict)
# ENCODED_DATA = fc.FAIR_ENCODER(DATA, ENCODER_dict)
DECODER_dict = fc.DECODE_TO_DICT(RAW_vocab)
print(DECODER_dict)
# Fair Encoder
# encode_dict, decode_dict = fc.get_encode_decode_dictionaries(DATA)
# print("Unique Character Count:", len(encode_dict))

# """ Save to meta.pkl file. """
# meta = {
#     'vocab_size': vocab_size,
#     'decode': decode_dict,
#     'encode': encode_dict,
# }

# FILE.save_file(f'{cwd}/{OUT_DIR}/vocab_raw', RAW_vocab)
FILE.save_file_json(f'{cwd}/vocab_encoder', ENCODER_dict)
FILE.save_file_json(f'{cwd}/vocab_decoder', DECODER_dict)
# with open(f'{cwd}/{OUT_DIR}/meta.pkl', 'wb') as f:
#     pickle.dump(meta, f)

# # Create Training Data as well.
# if CREATE_TRAINING_DATA_SET:
#     e_coder = Faircoder.encoder_from_vocab(f'{cwd}/{OUT_DIR}/meta.pkl')
#     ENCODED_DATA = e_coder(DATA)
#
#     # TORCH_DATA = torch.tensor(ENCODED_DATA, dtype=torch.long)
#     train_data = ENCODED_DATA[:int(vocab_size * 0.9)]
#     val_data = ENCODED_DATA[int(vocab_size * 0.9):]
#
#     # export to bin files
#     train_ids = np.array(train_data, dtype=np.uint16)
#     val_ids = np.array(val_data, dtype=np.uint16)
#     train_ids.tofile(f'{cwd}/{OUT_DIR}/train.bin')
#     val_ids.tofile(f'{cwd}/{OUT_DIR}/val.bin')



""" as of Jan 19 2022 -> 735,829 articles plus All Shakespeare
Vocab Size: 3,548,578,809 (~3.5 Billion Overall Characters Analyzed)
Unique Character Count: 15,929 (~16 Thousand Unique Characters)
"""