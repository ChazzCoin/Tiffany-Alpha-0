import numpy as np
from TheBrain.BrainDB.ArticleProvider import Provider
from F import OS
from TheBrain.GPT import Faircoder
cwd = OS.get_cwd()


def get_data_set():
    _DATA = ""
    # Shakespeare
    with open('in/input.txt', 'r') as f:
        _DATA += f.read()

    """ GET ARTICLES """
    db = Provider()
    result = db.get_articles(limit=10)
    print("Article Count:", len(result))
    for art in result:
        temp_all = str(art)
        _DATA += temp_all
    return _DATA


DATA = get_data_set()
n = len(DATA)
train_data = DATA[:int(n*0.9)]
val_data = DATA[int(n*0.9):]

e_coder = Faircoder.encoder_from_vocab(f'{cwd}/out/meta.pkl')
train_ids = e_coder(train_data)
val_ids = e_coder(val_data)

# export to bin files
train_ids = np.array(train_ids, dtype=np.uint16)
val_ids = np.array(val_ids, dtype=np.uint16)
train_ids.tofile(f'{cwd}/out/train.bin')
val_ids.tofile(f'{cwd}/out/val.bin')