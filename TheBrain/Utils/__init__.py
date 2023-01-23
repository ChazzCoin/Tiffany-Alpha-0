import pickle


def load_pickle_file(picklePath):
    with open(picklePath, 'rb') as f:
        pkl = pickle.load(f)
    return pkl

def save_pickle_file(picklePath, pickleFile):
    with open(picklePath, 'wb') as f:
        pickle.dump(pickleFile, f)