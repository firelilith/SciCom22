import numpy as np

from typing import List, Callable


def rk4_step(funcs, timestep, vals, constants):
    k1 = np.zeros(shape=vals.shape)
    k2 = np.zeros(shape=vals.shape)
    k3 = np.zeros(shape=vals.shape)
    k4 = np.zeros(shape=vals.shape)

    for i, f in enumerate(funcs):
        print(k1)
        k1[:, i] = f(0, vals, constants)
        k2[:, i] = f(timestep/2, vals + timestep/2 * k1, constants)
        k3[:, i] = f(timestep/2, vals + timestep/2 * k2, constants)
        k4[:, i] = f(timestep, vals + timestep * k3, constants)

    return vals + timestep*(k1 + 2*k2 + 2*k3 + k4)/6


def integrate(funcs: List[Callable], starting_vals: np.ndarray, timestep: float, time: float):
    vals = starting_vals.copy()
    for i in range(int(time/timestep+1)):
        vals = rk4_step(funcs, timestep, vals)
        yield vals
