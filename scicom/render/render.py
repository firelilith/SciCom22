import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import argparse
from itertools import zip_longest
from contextlib import ExitStack


def load_files(data_files):
    with ExitStack() as stack:
        files = [stack.enter_context(open(f, "r")) for f in data_files]
        for step in zip_longest(*files):
            step = tuple(map(str.strip, step))
            yield np.fromstring(" ".join(step), dtype=int, sep=" ").reshape(-1, 4).T


def plot(files, dpi, out_file):
    def update_figure(p, d):
        p.set_data(d[0], d[1])
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)

    data = load_files(files)

    fig, ax = plt.subplots(1, 1)

    l, = ax.plot([], [])

    writer = animation.FFMpegWriter(fps=15)
    with writer.saving(fig=fig, outfile=out_file, dpi=dpi):
        for step in data:
            update_figure(l, step)
            writer.grab_frame()


if __name__ == "__main__":
    plot(["sample.txt"], 100, "out.mp4")

    parser = argparse.ArgumentParser(prog="render engine for nbody simulation")

    parser.add_argument("-s", "--style", type=str, required=False, default="./plotconfig.mplstyle",
                        help="A .mplstyle file containing syle data")

    args = parser.parse_args()

    # plt.style.use(args.style)
else:
    # plt.style.use("./plotconfig.mplstyle")
    pass
