import matplotlib.pyplot as plt
import matplotlib.style
from astropy import units

import numpy as np

from typing import Generator


def compare(series1: tuple[Generator[np.ndarray, None, None], np.ndarray[float], np.ndarray[float], np.ndarray[str]],
            series2: tuple[Generator[np.ndarray, None, None], np.ndarray[float], np.ndarray[float], np.ndarray[str]],
            *,
            show=True,
            strict=True):

    gen1, t1, m1, l1 = series1

    gen2, t2, m2, l2 = series2

    if not np.all(l1 == l2):
        raise ValueError("object labels need to be identical for comparison")
    # if not np.allclose(t1, t2, atol=1000):
    #     raise ValueError("times must be identical for comparison")
    if strict and not np.allclose(m1, m2):
        raise ValueError("strict mode enabled. masses need to be identical")

    fig, ax = plt.subplots()
    delta = np.array([np.linalg.norm((x1 - x2)[:, :3], axis=1) for x1, x2 in zip(gen1, gen2)]).T

    t1 = list(t1)

    for val, name in zip(delta, l1):
        ax.plot(t1, val, label=name)

    plt.legend()
    if show:
        plt.show()

    return fig, ax


def topdown(series: tuple[Generator[np.ndarray, None, None], np.ndarray[float], np.ndarray[float], np.ndarray[str]],
            show: bool = True, radius: float = 2):
    matplotlib.style.use("dark_background")
    val_gen, times, masses, labels = series

    fig, ax = plt.subplots()
    x_vals = []
    y_vals = []

    for val in val_gen:
        x_vals.append(val[:, 0])
        y_vals.append(val[:, 1])

    x_vals = np.array(x_vals).T * units.meter.to(units.AU)
    y_vals = np.array(y_vals).T * units.meter.to(units.AU)

    plt.grid(True, c="#303030")

    for x, y, label in zip(x_vals, y_vals, labels):
        ax.plot(x, y, label=label)

    ax.set_prop_cycle(None)

    for x, y, m, l in zip(x_vals, y_vals, masses, labels):
        s = np.log(m/np.min(masses)) + 1
        ax.scatter(x[-1], y[-1], s=2*s)
        ax.text(x[-1], y[-1], f"  {l}")

    max_lim = max(np.max(np.abs(x_vals)), np.max(np.abs(y_vals))) * 1.1

    if radius:
        max_lim = radius

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-max_lim, max_lim)
    ax.set_ylim(-max_lim, max_lim)
    # ax.legend()

    if show:
        plt.show()

    return fig, ax


def topdown_cmp(series1: tuple[
                    Generator[np.ndarray, None, None], np.ndarray[float], np.ndarray[float], np.ndarray[str]],
                series1_name: str,
                series2: tuple[
                    Generator[np.ndarray, None, None], np.ndarray[float], np.ndarray[float], np.ndarray[str]],
                series2_name: str,
                series3: tuple[
                    Generator[np.ndarray, None, None], np.ndarray[float], np.ndarray[float], np.ndarray[str]] = None,
                series3_name: str = None,
                radius: float = 2,
                show: bool = True):

    gen1, t1, m1, l1 = series1
    gen2, t2, m2, l2 = series2

    matplotlib.style.use("dark_background")

    fig, ax = plt.subplots()
    x_vals1 = []
    y_vals1 = []

    x_vals2 = []
    y_vals2 = []

    for val in gen1:
        x_vals1.append(val[:, 0])
        y_vals1.append(val[:, 1])

    for val in gen2:
        x_vals2.append(val[:, 0])
        y_vals2.append(val[:, 1])

    x_vals1 = np.array(x_vals1).T * units.meter.to(units.AU)
    y_vals1 = np.array(y_vals1).T * units.meter.to(units.AU)

    x_vals2 = np.array(x_vals2).T * units.meter.to(units.AU)
    y_vals2 = np.array(y_vals2).T * units.meter.to(units.AU)

    plt.grid(True, c="#303030")

    for x, y in zip(x_vals1, y_vals1):
        ax.plot(x, y)

    ax.set_prop_cycle(None)

    for x, y, m, l in zip(x_vals1, y_vals1, m1, l1):
        s = np.log(m / np.min(m1)) + 1
        ax.scatter(x[-1], y[-1], s=2 * s)
        ax.text(x[-1], y[-1], f"  {l}")

    ax.set_prop_cycle(None)

    for x, y in zip(x_vals2, y_vals2):
        ax.plot(x, y, "--")

    ax.set_prop_cycle(None)

    for x, y, m in zip(x_vals2, y_vals2, m2):
        s = np.log(max(m, 1) / max(np.min(m2), 1)) + 1
        ax.scatter(x[-1], y[-1], s=2 * s)

    max_lim1 = max(np.max(np.abs(x_vals1)), np.max(np.abs(y_vals1))) * 1.1
    max_lim2 = max(np.max(np.abs(x_vals2)), np.max(np.abs(y_vals2))) * 1.1
    max_lim = max(max_lim1, max_lim2)

    ax.plot(0, 0, "-w", label=series1_name)
    ax.plot(0, 0, "--w", label=series2_name)

    if series3 is not None:
        gen3, t3, m3, l3 = series3

        x_vals3 = []
        y_vals3 = []

        for val in gen3:
            x_vals3.append(val[:, 0])
            y_vals3.append(val[:, 1])

        x_vals3 = np.array(x_vals3).T * units.meter.to(units.AU)
        y_vals3 = np.array(y_vals3).T * units.meter.to(units.AU)

        ax.set_prop_cycle(None)

        for x, y in zip(x_vals3, y_vals3):
            ax.plot(x, y, ":")

        ax.set_prop_cycle(None)

        for x, y, m in zip(x_vals3, y_vals3, m3):
            s = np.log(m / np.min(m3)) + 1
            ax.scatter(x[-1], y[-1], s=2 * s)

        ax.plot(0, 0, ":w", label=series3_name)

        max_lim3 = max(np.max(np.abs(x_vals3)), np.max(np.abs(y_vals3))) * 1.1
        max_lim = max(max_lim, max_lim3)

    if radius:
        max_lim = radius

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-max_lim, max_lim)
    ax.set_ylim(-max_lim, max_lim)
    ax.legend()

    if show:
        plt.show()

    return fig, ax
