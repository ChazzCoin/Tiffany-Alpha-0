from TheBrain.BrainDB.ArticleProvider import Provider
from F import OS, FILE, DICT

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
        title = DICT.get("title", art, "")
        body = DICT.get("body", art, "")
        temp_all = str(title) + " " + str(body)
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
