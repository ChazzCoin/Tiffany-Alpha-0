from TheBrain.BrainDB.ArticleProvider import Provider
from F import OS, FILE

cwd = OS.get_cwd()

i = FILE.get_file_path(__file__=__file__)

def get_raw_data_set(articleLimit=10) -> str:
    _DATA = ""
    # Shakespeare
    # with open(f'{i}/VocabGenerators/input.txt', 'r') as f:
    #     _DATA += f.read()

    """ GET ARTICLES """
    db = Provider()
    result = db.get_articles(limit=articleLimit)
    print("Article Count:", len(result))
    for art in result:
        temp_all = str(art)
        _DATA += temp_all
    return _DATA

def get_raw_train_and_val(raw_data=None) -> ([],[]):
    if raw_data:
        DATA = raw_data
    else:
        DATA = get_raw_data_set()
    n = len(DATA)
    train_data = DATA[:int(n*0.9)]
    val_data = DATA[int(n*0.9):]
    return train_data, val_data

# e_coder = Faircoder.encoder_from_vocab(f'{cwd}/out/meta.pkl')
# train_ids = e_coder(train_data)
# val_ids = e_coder(val_data)

# def to_file(encoded_data):
#     # export to bin files
#     train_ids = np.array(train_ids, dtype=np.uint16)
#     val_ids = np.array(val_ids, dtype=np.uint16)
#     train_ids.tofile(f'{cwd}/out/train2.bin')
#     val_ids.tofile(f'{cwd}/out/val2.bin')