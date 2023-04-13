import datetime
import logging

import newton
import post_newton_eih
import render.plotting
from library import solar_system_reference
from library.file_io import save_series, load_series
from library.iterhelp import sparsify
from library import coords, file_io
from render.renderlib import animate
from render.plotting import *

import multiprocessing

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def re_save(path, target, timestep):
    series = load_series(path)
    new = sparsify(series, timestep)
    save_series(target, new)


bodies = solar_system_reference.solar_system_bodies

preset = solar_system_reference.solar_system(bodies=bodies, trust_v=False)
# preset = file_io.load_yaml_preset("examples/black_hole_comet.yml")

t = 500 * 365 * 24 * 3600 / 10000
tolerance = 10000000

series1 = newton.adaptive_nbody(*preset, dt=1000, time=t, tolerance=tolerance)
series2 = post_newton_eih.adaptive_nbody(*preset, dt=1000, time=t, tolerance=tolerance)

# ref = solar_system_reference.get_series(bodies=bodies, duration=t, dt=10000)


first = multiprocessing.Process(target=lambda: re_save("series/250y_newt.csv", "series/500y_newt_sparse.csv", 24*3600))
second = multiprocessing.Process(target=lambda: re_save("series/250y_post.csv", "series/500y_post_sparse.csv", 24*3600))

# first = multiprocessing.Process(target=lambda: save_series("series/250y_newt.csv", series1))
# second = multiprocessing.Process(target=lambda: save_series("series/250y_post.csv", series2))

first.start()
second.start()
first.join()
second.join()

#topdown_cmp(series1=series1, series1_name="newt",
#            series2=series2, series2_name="post",
#            show=True, radius=None)
