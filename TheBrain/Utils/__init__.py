import pickle


def load_pickle_file(picklePath):
    with open(picklePath, 'rb') as f:
        pkl = pickle.load(f)
    return pkl