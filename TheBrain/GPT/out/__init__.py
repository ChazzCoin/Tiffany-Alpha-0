from F import OS
from TheBrain import Utils


OUT_PATH = OS.get_path(__file__=__file__)
_training_name = "train.bin"
_val_name = "val.bin"
_checkpoint_name = "ckpt.pt"
OUT_FILE_GETTER = lambda name: f"{OUT_PATH}/{name}"

def get_training_data():
    return Utils.load_pickle_file(OUT_FILE_GETTER(_training_name))

def save_training_data():
    pass

