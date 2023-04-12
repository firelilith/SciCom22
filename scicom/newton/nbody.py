import numpy as np

from functools import partial

from astropy import constants

from scicom.library.rk4 import rk4_integration, rkf45_integration
from scicom.library.coords import distance_vec, distance_sca
from scicom.library.unit_helpers import unit_setup
from scicom.library.iterhelp import split_generator


def nbody(positions, velocities, masses, labels, dt, time):
    x, v, m = unit_setup(positions, velocities, masses)
    ode = partial(_diff_eq, m=m)
    vals = np.concatenate((x, v), axis=-1)

    return (rk4_integration(ode=ode, start_vals=vals, dt=dt, stop_time=time),
            np.linspace(0, time, int(time/dt), endpoint=False),
            m,
            labels)


def adaptive_nbody(positions, velocities, masses, labels, dt, time, tolerance, **kwargs):
    x, v, m = unit_setup(positions, velocities, masses)
    ode = partial(_diff_eq, m=m)
    vals = np.concatenate((x, v), axis=-1)

    integration = rkf45_integration(ode, vals, dt, time, tolerance, **kwargs)

    locations, times = split_generator(integration)

    return (locations,
            times,
            m,
            labels)


def _diff_eq(vals, m):
    """Newtonian acceleration: a = Gmr/|r|^3 """
    out = np.zeros(vals.shape)
    out[..., :3] = vals[..., 3:]

    # numpy black magic, sorry not sorry
    dist = distance_vec(vals[..., :3])
    dist_sca = distance_sca(vals[..., :3])

    with np.errstate(divide="ignore", invalid="ignore"):
        acc = (constants.G.value * m[None, :, None] * dist /
               (dist_sca ** 3)[:, :, None])

    acc[~np.isfinite(acc)] = 0
    out[..., 3:] = np.sum(acc, axis=1)
    return out

