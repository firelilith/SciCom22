import os

import yaml

import numpy as np

from astropy import units
from typing import Iterable


def load_yaml_preset(path: str):
    with open(path) as f:
        data = yaml.safe_load(f)

    masses = []
    positions = []
    velocities = []
    labels = []

    for key in data:
        space_unit = units.Unit(data[key]["units"]["position"])
        time_unit = units.Unit(data[key]["units"]["time"])
        mass_unit = units.Unit(data[key]["units"]["mass"])
        positions.append((data[key]["position"] * space_unit).to(units.m).value)
        velocities.append((data[key]["velocity"] * space_unit/time_unit).to(units.m/units.s).value)
        masses.append((data[key]["mass"] * mass_unit).to(units.kg))
        labels.append(key)

    return (np.array(positions) * units.meter,
            np.array(velocities) * units.meter/units.second,
            np.array(masses) * units.kg,
            labels)
        

def load_csv_preset(path: str):
    data = np.loadtxt(path, delimiter=",", dtype=str)

    if not data.shape[1] in {7, 8}:
        raise ValueError("CSV file needs to have 7 or 8 rows: x,x,x,v,v,v,m(,name)")

    return (np.array(data[:, :3], dtype=float) * units.meter,
            np.array(data[:, 3:6], dtype=float) * units.meter/units.second,
            np.array(data[:, 6], dtype=float) * units.kg,
            data[7] if data.shape[1] == 8 else [str(i) for i in range(data.shape[0])])


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


def load_multiple(paths: list[str]):
    for arr_list in zip(load_series(path) for path in paths):
        yield np.concatenate(arr_list, axis=0)


def _dump_2d(arr: np.array):
    return ";".join(",".join(i for i in j) for j in arr)


def _load_2d(arr: str):
    return np.array([[i for i in j.split(",")] for j in arr.split(";")], dtype=float)
