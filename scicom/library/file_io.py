import logging
import os

import yaml

import numpy as np

from astropy import units
from typing import Iterable

from scicom.library.iterhelp import split_generator


logger = logging.getLogger(__name__)


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


def save_series(path: str,
                series: tuple[Iterable[np.ndarray], np.ndarray[float], np.ndarray[float],  np.ndarray[str]],
                overwrite=False):
    if os.path.exists(path) and not overwrite:
        raise FileExistsError("give new file path, or set overwrite to True")

    steps, times, masses, labels = series


    with open(path, "w") as f:
        f.write(",".join(labels) + "\n")
        f.write(",".join(str(m) for m in masses) + "\n")
        for i, (t, arr) in enumerate(zip(times, steps)):
            if i % 100 == 0:
                logger.debug(f"wrote step {i} to {path}")
            f.write(f"{t}:{_dump_2d(arr)}\n")


def load_series(path: str):
    def gen(p):
        with open(p) as file:
            file.readline()
            file.readline()
            for line in file:
                t, rest = line.split(":")
                t = float(t)
                arr = _load_2d(rest)
                yield t, arr
    if not os.path.exists(path):
        raise FileNotFoundError

    with open(path) as f:
        labels = np.array(next(f).strip().split(","), dtype=str)
        masses = np.array(next(f).strip().split(","), dtype=float)
    times, steps = split_generator(gen(path))
    return steps, times, masses, labels


def load_multiple(paths: list[str]):
    def gen(list_of_generators):
        for arr_list in zip(*list_of_generators):
            yield np.concatenate(arr_list, axis=0)

    gen_list, mass_list, time_list, label_list = zip(*[load_series(path) for path in paths])

    masses = np.concatenate(mass_list)
    times = np.concatenate(time_list)
    labels = np.concatenate(label_list)

    return gen(gen_list), masses, labels


def _dump_2d(arr: np.array):
    return ";".join(",".join(str(i) for i in j) for j in arr)


def _load_2d(arr: str):
    return np.array([[i for i in j.split(",")] for j in arr.split(";")], dtype=float)
