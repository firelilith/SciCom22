import datetime
import logging

import newton
import post_newton_eih
import render.plotting
from library import solar_system_reference
from library import coords, file_io
from render.renderlib import animate
from render.plotting import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bodies = solar_system_reference.solar_system_bodies

preset = solar_system_reference.solar_system(bodies=bodies, trust_v=False)
preset = file_io.load_yaml_preset("examples/black_hole_comet.yml")

t = 5000000

series1 = newton.adaptive_nbody(*preset, dt=1000, time=t, tolerance=10000000)
series2 = post_newton_eih.adaptive_nbody(*preset, dt=1000, time=t, tolerance=10000000)

ref = solar_system_reference.get_series(bodies=bodies, duration=t, dt=10000)

topdown_cmp(series1=series1, series1_name="newt",
            series2=series2, series2_name="post",
            show=True, radius=None)
