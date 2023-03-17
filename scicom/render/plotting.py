import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np

from typing import Generator


def compare(series1: tuple[Generator[np.ndarray, None, None], np.ndarray[float], np.ndarray[float], np.ndarray[str]],
            series2: tuple[Generator[np.ndarray, None, None], np.ndarray[float], np.ndarray[float], np.ndarray[str]],
            *,
            strict=True):

    gen1, t1, m1, l1 = series1

    gen2, t2, m2, l2 = series2

    diff = t1 - t2

    if not np.all(l1 == l2):
        raise ValueError("object labels need to be identical for comparison")
    if not np.allclose(t1, t2):
        raise ValueError("times must be identical for comparison")
    if strict and not np.allclose(m1, m2):
        raise ValueError("strict mode enabled. masses need to be identical")

    fig = plt.figure()
    delta = np.array([np.linalg.norm((x1 - x2)[:, :3], axis=1) for x1, x2 in zip(gen1, gen2)]).T

    for val, name in zip(delta, l1):
        plt.plot(t1, val, label=name)

    plt.legend()
    plt.show()
