import os
import sys
import json
import yaml
import pickle
import itertools
import pandas as pd
from glob import glob
from typing import Dict, List, Tuple


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)


def load_data(path: str) -> Dict:
    if path.endswith("json"):
        with open(path, "r") as f:
            data = json.load(f)
            return data
    elif path.endswith("pkl") or path.endswith("pickle"):
        with open(path, "rb") as f:
            data = pickle.load(f)
            return data
    elif path.endswith("yaml") or path.endswith("yml"):
        with open(path, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data


def modify_data(path: str, data: Dict) -> Dict:
    # if you want to get specify data leave, use this function.
    # example:
    # new_data = {}
    # if path.endswith("summary.json"):
    #     new_data["AUROC"] = data["AUROC"]
    #     # return new_data
    # if path.endswith("stats.json"):
    #     data.pop("num_samples")
    #     new_data = data
    # return new_data
    return data


class LoopsNestedDictionary:
    def __init__(
        self,
        mother_root: str,
        root_names: List[str],
        *args,
        **kwargs,
    ):
        # note that kwargs has a order.
        self.mother_root = mother_root
        self.root_names = root_names
        self.all_keys = list(kwargs.keys())
        self.pairs = self.get_pairs(kwargs)

    def get_pairs(self, kwargs: Dict[str, List]) -> List[List[str]]:
        prod = itertools.product(*kwargs.values())
        return list(map(list, prod))

    def search(self, pair: List[str]) -> Tuple[str, List[str]]:
        all_data_from_a_pair = {}
        for root_name in self.root_names:
            new_pair = [self.mother_root] + pair
            new_pair.append("**")
            new_pair.append(root_name)
            p = "/".join(new_pair)
            g_all = glob(p, recursive=True)
            try:
                path = g_all[0]
            except IndexError:
                print(f"not found p: {p}")
                continue
            all_data_from_a_pair.update(
                modify_data(path, load_data(path))
            )
        return "/".join(pair), all_data_from_a_pair

    def to_dict(self) -> Dict:
        result_list = []
        for pair in self.pairs:
            collect = {
                key: pair[i]
                for i, key in enumerate(self.all_keys)
            }
            pair, all_data_from_a_pair = self.search(pair)
            collect.update(all_data_from_a_pair)
            result_list.append(collect)
        df = pd.DataFrame(result_list)
        return df


if __name__ == "__main__":
    dataset = ["dataset1", "dataset2"]
    models = ["model1", "model2", "model3"]
    root_names = ["summary.json", "stats.json"]
    looper = LoopsNestedDictionary(
        mother_root=".",
        root_names=root_names,
        dataset=dataset,
        models=models,
    )
    df = looper.to_dict()
    print(df)
