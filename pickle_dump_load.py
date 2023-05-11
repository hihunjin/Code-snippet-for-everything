from typing import Any
import pickle


def pickle_dump(path: str, data: Any) -> None:
    with open(path, "wb") as f:
        pickle.dump(data, f)


def pickle_load(path: str) -> Any:
    with open(path, "rb") as f:
        return pickle.load(f)
