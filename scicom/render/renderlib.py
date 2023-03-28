import functools
import os.path

from multiprocessing import Pool

import logging

import matplotlib.pyplot as plt
import matplotlib.transforms
import numpy as np

from matplotlib import animation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _gen_image(num, image_dir, vals, plot_func, masses, times, labels, kwargs):
    new_gens = list(map(lambda k: (vals[k][j] for j in range(num)),
                        range(len(vals))))

    new_series = [(new_gens[k], times[k][:num], masses[k], labels[k]) for k in range(len(vals))]
    fig, ax = plot_func(*new_series, show=False, **kwargs)

    path = os.path.join(image_dir, f"{num:0>5}.png")
    if num % 10 == 0:
        logger.info(f"writing image {num}")
    plt.xlim(ax.get_xlim())
    plt.ylim(ax.get_ylim())
    fig.savefig(path, format="png", dpi=800, bbox_inches="tight")
    plt.close()


def animate(plot_func: callable, *series, out: str = None, image_dir: str = None, **kwargs):
    gens, times, masses, labels = zip(*series)

    vals = [list(gen) for gen in gens]

    tmp_dir = os.path.join(os.path.dirname(__file__), "tmp")

    if image_dir is None:
        image_dir = tmp_dir

    func = functools.partial(_gen_image,
                             image_dir=image_dir,
                             vals=vals,
                             plot_func=plot_func,
                             masses=masses,
                             times=times,
                             labels=labels,
                             kwargs=kwargs)

    with Pool(4) as pool:
        pool.map(func, range(1, len(vals[0])))

    logger.info(f"writing video to {out}")
    os.system(f"ffmpeg -y -v 3 -framerate 30 -pattern_type glob -i '{image_dir}/*.png' -s 1200x1200 {out}")


"""
    for file in os.listdir(tmp_dir):
        os.remove(os.path.join(tmp_dir, file))
"""