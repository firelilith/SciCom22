import os

import yaml

import numpy as np

from typing import Iterable


def load_yaml_preset(path: str):
    with open(path) as f:
        data = yaml.safe_load(f)


def load_csv_preset(path: str):
    data = np.loadtxt(path, delimiter=",", dtype=str)

    if not data.shape[1] in {7, 8}:
        raise ValueError("CSV file needs to have 7 or 8 rows")


def save_series(path: str, series: Iterable[np.array], overwrite=False):
    if os.path.exists(path) and not overwrite:
        raise FileExistsError("give new file path, or set overwrite to True")
    with open(path, "w") as f:
        for arr in series:
            f.write(_dump_2d(arr))
            f.write("\n")


def load_series(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError

    with open(path) as f:
        for line in f:
            yield _load_2d(line)


def _dump_2d(arr: np.array):
    return ";".join(",".join(i for i in j) for j in arr)


def _load_2d(arr: str):
    return np.array([[i for i in j.split(",")] for j in arr.split(";")], dtype=float)
