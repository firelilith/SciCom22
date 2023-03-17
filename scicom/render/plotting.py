import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np

from typing import Generator


def compare(series1: tuple[Generator[np.ndarray, None, None], np.ndarray[float], np.ndarray[float], np.ndarray[str]],
            series2: tuple[Generator[np.ndarray, None, None], np.ndarray[float], np.ndarray[float], np.ndarray[str]],
            *,
            show=False,
            strict=True):

    gen1, t1, m1, l1 = series1

    gen2, t2, m2, l2 = series2

    if not np.all(l1 == l2):
        raise ValueError("object labels need to be identical for comparison")
    if not np.allclose(t1, t2):
        raise ValueError("times must be identical for comparison")
    if strict and not np.allclose(m1, m2):
        raise ValueError("strict mode enabled. masses need to be identical")

    fig, ax = plt.subplots()
    delta = np.array([np.linalg.norm((x1 - x2)[:, :3], axis=1) for x1, x2 in zip(gen1, gen2)]).T

    for val, name in zip(delta, l1):
        ax.plot(t1, val, label=name)

    plt.legend()
    if show:
        plt.show()

    return fig, ax


def topdown(series: tuple[Generator[np.ndarray, None, None], np.ndarray[float], np.ndarray[float], np.ndarray[str]],
            show: bool = True):
    val_gen, times, masses, labels = series

    fig, ax = plt.subplots()
    x_vals = []
    y_vals = []

    for val in val_gen:
        x_vals.append(val[:, 0])
        y_vals.append(val[:, 1])

    x_vals = np.array(x_vals).T
    y_vals = np.array(y_vals).T

    for x, y, label in zip(x_vals, y_vals, labels):
        ax.plot(x, y, label=label)

    ax.set_prop_cycle(None)

    for x, y, m in zip(x_vals, y_vals, masses):
        s = np.log(m/np.min(masses)) + 1
        ax.scatter(x[-1], y[-1], s=5*s)

    ax.legend()

    if show:
        plt.show()

    return fig, ax
