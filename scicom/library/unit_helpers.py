from astropy import units

import numpy as np

import logging

logger = logging.getLogger(__name__)


def unit_setup(x, v, m):
    if not type(x) == units.Quantity:
        x = np.array(x)
        logger.warning("no unit given for position, assuming meter")
    else:
        x = np.array(x.to(units.meter).value)
    if not type(v) == units.Quantity:
        v = np.array(v)
        logger.warning("no unit given for velocity, assuming meter/second")
    else:
        v = np.array(v.to(units.meter/units.second).value)
    if not type(m) == units.Quantity:
        m = np.array(m)
        logger.warning("no unit given for mass, assuming kilogram")
    else:
        m = np.array(m.to(units.kg).value)

    return x, v, m
