from library.iterhelp import sparsify
from library.file_io import save_series
from library.solar_system_reference import solar_system

import newton
import post_newton_eih

import multiprocessing

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(processName)s:%(module)s: %(message)s")
logger = logging.getLogger(__name__)

preset = solar_system()

time = 10000 * 365 * 24 * 3600
tolerance = 100000000

newt = newton.adaptive_nbody(*preset, dt=1000, time=time, tolerance=tolerance)
post = post_newton_eih.adaptive_nbody(*preset, dt=1000, time=time, tolerance=tolerance)

p1 = multiprocessing.Process(target=lambda: save_series("series/10ky_newt.csv", sparsify(newt, 5 * 24 * 3600)))
p2 = multiprocessing.Process(target=lambda: save_series("series/10ky_post.csv", sparsify(post, 5 * 24 * 3600)))

p1.start()
p2.start()

p1.join()
p2.join()
