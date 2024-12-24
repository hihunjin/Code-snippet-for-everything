import json
import pickle
import numpy as np
from typing import Any


def pickle_dump(path: str, data: Any) -> None:
    with open(path, "wb") as f:
        pickle.dump(data, f)


def pickle_load(path: str) -> Any:
    with open(path, "rb") as f:
        return pickle.load(f)


def npy_save(path: str, data: np.ndarray) -> None:
    with open(path, "wb") as f:
        np.save(f, data)


def npy_load(path: str) -> np.ndarray:
    with open(path, "rb") as f:
        return np.load(f)


def save_json(p, data) -> None:
    with open(p, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def load_json(p: str) -> Any:
    try:
        with open(p) as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f"Error: {e} on {p}")
        raise e
