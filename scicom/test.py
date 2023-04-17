import datetime
import logging

import newton
import post_newton_eih
import render.plotting
from library import solar_system_reference
from library.file_io import save_series, load_series
from library.iterhelp import sparsify, head, tail
from library import coords, file_io
from render.renderlib import animate
from render.plotting import *

from itertools import tee

import multiprocessing

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def re_save(path, target, timestep):
    series = load_series(path)
    new = sparsify(series, timestep)
    save_series(target, new)


# first = multiprocessing.Process(target=lambda: re_save("series/250y_newt.csv", "series/500y_newt_sparse.csv", 24*3600))
# second = multiprocessing.Process(target=lambda: re_save("series/250y_post.csv", "series/500y_post_sparse.csv", 24*3600))

# s1, s2 = tee(load_series("series/500y_post_sparse.csv"))

#series1 = tail(load_series("series/10ky_post.csv"), 10)
#series2 = tail(load_series("series/10ky_newt.csv"), 10)


# series1 = head(s1, 100)
# series2 = tail(s2, 100)
"""
for i in series1[0]:
    print("head: ", i)

for i in series2[0]:
    print("tail: ", i)"""


start = solar_system_reference.solar_system()
series = newton.adaptive_nbody(*start, dt=200, time = 10000000, tolerance=1000000)
topdown(series)

# compare(series1, series2)

#topdown_cmp(series1=series1, series1_name="post",
#            series2=series2, series2_name="newt",
#            radius=.5)
