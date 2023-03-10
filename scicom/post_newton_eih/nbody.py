import astropy.units
import numpy as np
import logging

from functools import partial
from astropy import constants, units

from scicom.library import rk4_integration, distance_sca, distance_vec, distance_unt


logger = logging.getLogger(__name__)


def nbody(pos, vel, mas, dt, time):
    if not type(pos) == units.Quantity:
        pos = pos * units.meter
        logger.warning("no units given for position. assuming m")
    else:
        pos = pos.to(units.meter)

    if not type(vel) == units.Quantity:
        vel = vel * units.meter / units.second
        logger.warning("no units given for velocity. assuming m/s")
    else:
        vel = vel.to(units.meter / units.second)

    if not type(mas) == units.Quantity:
        mas = mas * units.kg
        logger.warning("no units given for mass. assuming kg")
    else:
        mas = mas.to(units.kg)


def _diff_eq(m: np.array, vals: np.array):
    m = m * units.kg  # TODO: remove type annotations in _diff_eq

    iterations = 5

    out = np.zeros(vals.shape)

    out[..., :3] = vals[..., 3:]

    # calculate common values
    dist_vec = distance_vec(vals[..., :3]) * units.meter
    dist_sca = distance_sca(vals[..., :3]) * units.meter
    unit_vec = distance_unt(vals[..., :3]) * units.meter / units.meter
    v_vec = vals[..., 3:] * units.meter / units.second
    v_prod = np.tensordot(vals[..., 3:], vals[..., 3:], axes=((1,), (1,))) * units.meter ** 2 / units.second ** 2
    v_sqrd = np.diagonal(v_prod)
    # nABvB = np.tensordot(unit_vec, v_vec[:, None, :], axes=((1, 2), (1, 2)))
    nABvB = np.sum(unit_vec * v_vec[None, :, :], axis=2)

    with np.errstate(divide="ignore", invalid="ignore"):
        n_acc = (constants.G * m[:, None, None] * dist_vec /
                 (dist_sca ** 3)[:, :, None])
    n_acc[~np.isfinite(n_acc)] = 0

    n_acc_sum = np.sum(n_acc, axis=1)

    acc = n_acc_sum.copy()

    with np.errstate(divide="ignore", invalid="ignore"):
        nested = 4 * constants.G * m[:, None] / dist_sca
    nested[~np.isfinite(nested)] = 0

    #  https://en.wikipedia.org/wiki/Einstein%E2%80%93Infeld%E2%80%93Hoffmann_equations
    with np.errstate(divide="ignore", invalid="ignore"):
        for i in range(iterations):
            new_acc = np.zeros(n_acc_sum.shape) * units.meter / units.second ** 2

            a = 1/2 * np.tensordot(dist_vec, acc, axes=((2,), (1,)))
            b = 1/2 * np.sum(dist_vec * acc[None, :, :], axis=2)

            first_term = (np.ones(1)[:, None]
                          + 1 / constants.c ** 2 * (
                            v_sqrd[:, None]
                            + 2 * v_sqrd[None, :]
                            + 4 * v_prod[:, :]
                            - 3/2 * nABvB ** 2
                            + 1/2 * np.tensordot(dist_vec, acc, axes=((1, 2), (0, 1)))[:, None]  # this is very clearly wrong
                            - np.sum(nested, axis=1))  # TODO: check if right axis
                          )
            first_term[~np.isfinite(first_term)] = 0
            new_acc += np.sum(n_acc * first_term[:, :, None], axis=1)

            second_term = (m[:, None, None] / dist_sca[:, :, None]**2
                           * ((np.sum(unit_vec * (4 * v_vec[None, :, :] - 3 * v_vec[:, None, :]), axis=2))[:, :, None]
                           * (v_vec[None, :, :] - v_vec[:, None, :])))
            second_term[~np.isfinite(second_term)] = 0
            new_acc += -constants.G / constants.c**2 * np.sum(second_term, axis=1)

            third_term = m[:, None, None] * acc[:, None, :] / dist_sca[:, :, None]
            third_term[~np.isfinite(third_term)] = 0
            new_acc += constants.G * 7 / (2 * constants.c**2) * np.sum(third_term, axis=1)

            if np.all(new_acc - acc == 0):
                break
            acc = new_acc

    out[..., 3:] = acc
    return out

