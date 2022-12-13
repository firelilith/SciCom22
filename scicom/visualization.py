import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from typing import Generator, Union, Iterable

matplotlib.use("qtagg")


def animate(simulation: Generator[np.ndarray, None, None],
            masses=None,
            alpha=0.7,
            repeat=False,
            output_file=None):

    first = simulation.__next__()
    locations = first[0]

    if masses is not None:
        with np.errstate(divide="ignore"):
            color = np.log10(masses)
            color[~np.isfinite(color)] = 0
    else:
        color = 1

    def update(d, s, a):
        s._offsets3d = d[0].T

    locations = locations.T

    fig = plt.figure()
    ax = plt.axes(projection="3d")

    sc = ax.scatter(*locations, s=10, alpha=alpha, cmap="jet")

    ani = FuncAnimation(fig,
                        update,
                        frames=simulation,
                        fargs=(sc, ax),
                        repeat=repeat,
                        interval=0.001)

    if color is not None:
        clr = plt.colorbar(sc)

    if output_file:
        ani.save(output_file, "ffmpeg")
    else:
        plt.show()
