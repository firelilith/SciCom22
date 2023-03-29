import datetime
import logging

import newton
from post_newton_eih.nbody import _naive
import render.plotting
from library import solar_system_reference
from library import coords, file_io
from render.renderlib import animate
from render.plotting import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

preset = file_io.load_yaml_preset("examples/sun_comet.yml")

series = newton.adaptive_nbody(*preset, 1000, 150000000, 10000000)

topdown(series, show=True, radius=None)
