import numpy as np

from functools import partial
from scipy.constants import G

from scicom.library import rk4_integration


def nbody(pos, vel, mas, dt, time):
    ode = partial(_diff_eq, m=mas)
    vals = np.concatenate((pos, vel), axis=-1)

    return rk4_integration(ode=ode, start_vals=vals, dt=dt, stop_time=time)


def _diff_eq(vals, m):
    """Newtonian acceleration: a = Gm/r^2 """
    out = np.zeros(vals.shape)
    out[..., :3] = vals[..., 3:]

    # numpy black magic, sorry not sorry
    dist = vals[..., :3] - vals[..., :3].reshape((-1, 1, 3))
    with np.errstate(divide="ignore", invalid="ignore"):
        acc = (-1 * m * dist / np.sqrt(np.sum(
                np.square(dist),
                axis=2
            )**3)
        )
    out[..., 3:] = np.sum(acc[np.isfinite(acc)])
    return out
