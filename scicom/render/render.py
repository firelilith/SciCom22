import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np

from typing import Iterable, Generator


def compare(series1: tuple[Generator[np.ndarray, None, None], np.ndarray[float], np.ndarray[float], np.ndarray[str]],
            series2: tuple[Generator[np.ndarray, None, None], np.ndarray[float], np.ndarray[float], np.ndarray[str]],
            *,
            strict=True):

    gen1, m1, t1, l1 = series1
    gen2, m2, t2, l2 = series2

    if strict:
        if not (np.allclose(m1, m2) and np.all(l1 == l2)):
            raise ValueError("strict mode enabled. masses and labels need to be identical")

    fig = plt.figure()