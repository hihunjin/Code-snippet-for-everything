import numpy as np

def save_npz(filename: str, **kwargs):
    print("Saving to", filename)
    np.savez(filename, **kwargs)
    np.savez_compressed(filename, **kwargs)


def load_npz(filename: str):
    return np.load(filename)
