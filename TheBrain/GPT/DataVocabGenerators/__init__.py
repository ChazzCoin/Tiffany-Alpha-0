from F import FILE, OS

cwd = FILE.get_file_path(__file__=__file__)
def load_fair_encoder():
    return FILE.load_file_json(f"{cwd}/vocab_encoder")

def load_fair_decoder():
    return FILE.load_file_json(f"{cwd}/vocab_decoder")