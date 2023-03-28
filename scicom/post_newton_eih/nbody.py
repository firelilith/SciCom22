import numpy as np

from functools import partial
from astropy import constants, units

from scicom.library.rk4 import rk4_integration
from scicom.library.coords import distance_vec, distance_sca, distance_unt
from scicom.library.unit_helpers import unit_setup

import logging

import rustlib

logger = logging.getLogger(__name__)


def nbody(positions, velocities, masses, labels, dt, time):
    x, v, m = unit_setup(positions, velocities, masses)
    ode = partial(rustlib.post_newt_diff_eq, mass=m, c=constants.c.value, g=constants.G.value, max_iter=5)
    vals = np.concatenate((x, v), axis=1)

    return (rk4_integration(lambda pv: np.array(ode(pv)), vals, dt, time),
            np.linspace(0, time, int(time/dt), endpoint=False),
            m,
            labels)


def old_nbody(positions, velocities, masses, labels, dt, time):
    x, v, m = unit_setup(positions, velocities, masses)
    ode = partial(_naive, mas=masses)
    vals = np.concatenate((x, v), axis=1)

    return (rk4_integration(lambda pv: np.array(ode(pv)), vals, dt, time),
            np.linspace(0, time, int(time/dt), endpoint=False),
            m,
            labels)



def _diff_eq(m: np.array, vals: np.array):
    m = m * units.kg  # TODO: remove type annotations in _diff_eq

    max_iterations = 5

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
        for i in range(max_iterations):
            new_acc = np.zeros(n_acc_sum.shape) * units.meter / units.second ** 2

            a = 1/2 * np.tensordot(dist_vec, acc, axes=((2,), (1,)))
            b = 1/2 * np.sum(dist_vec * acc[None, :, :], axis=2)

            first_term = (np.ones(1)[:, None]
                          + 1 / constants.c ** 2 * (
                            v_sqrd[:, None]
                            + 2 * v_sqrd[None, :]
                            + 4 * v_prod[:, :]
                            - 3/2 * nABvB ** 2
                            + 1/2 * np.tensordot(dist_vec, acc, axes=((1, 2), (0, 1)))[:, None]  # this is very clearly wrong... der bär?
                            - np.sum(nested, axis=1))  # TODO: check if right axis
                          )
            first_term[~np.isfinite(first_term)] = 0
            new_acc += np.sum(n_acc * first_term[:, :, None], axis=1)

            second_term = (m[None, :, None] / dist_sca[:, :, None]**2
                           * ((np.sum(unit_vec * (4 * v_vec[None, :, :] - 3 * v_vec[:, None, :]), axis=2))[:, :, None]
                           * (v_vec[None, :, :] - v_vec[:, None, :])))
            second_term[~np.isfinite(second_term)] = 0
            new_acc += -constants.G / constants.c**2 * np.sum(second_term, axis=1)

            third_term = m[None, :, None] * acc[:, None, :] / dist_sca[:, :, None]
            third_term[~np.isfinite(third_term)] = 0
            new_acc += constants.G * 7 / (2 * constants.c**2) * np.sum(third_term, axis=1)

            if np.all(new_acc - acc == 0):
                break
            acc = new_acc

    out[..., 3:] = acc
    return out


def _naive(vals, mas):
    if type(mas) != np.ndarray:
        mas = np.array(mas.value)

    pos = vals[..., :3]
    vel = vals[..., 3:]

    out = np.zeros(vals.shape)
    out[:, :3] = vel

    old_acc = np.zeros(pos.shape)

    for i in range(5):

        acc = np.zeros(pos.shape)
        for a in range(len(mas)):
            for b in range(len(mas)):
                if a == b:
                    continue
                acc[a] += constants.G.value * mas[b] * (pos[b] - pos[a]) / np.linalg.norm(pos[b] - pos[a]) ** 3

        for a in range(len(mas)):
            for b in range(len(mas)):
                if a == b:
                    continue

                inner_1 = 0

                for c in range(len(mas)):
                    if a == c:
                        continue
                    inner_1 += constants.G.value * mas[c] / np.linalg.norm(pos[c] - pos[a])

                inner_2 = 0

                for c in range(len(mas)):
                    if b == c:
                        continue
                    inner_2 += constants.G.value * mas[c] / np.linalg.norm(pos[c] - pos[b])

                acc[a] += (1 / constants.c.value ** 2 * constants.G.value * mas[b]
                           * (pos[b] - pos[a]) / np.linalg.norm(pos[b] - pos[a]) ** 3 * (
                            np.dot(vel[a], vel[a]) + 2 * np.dot(vel[b], vel[b]) - 4 * np.dot(vel[a], vel[b])
                            + 3/2 * np.dot((pos[b] - pos[a]) / np.linalg.norm(pos[b] - pos[a]), vel[b]) ** 2
                            + 1/2 * np.dot((pos[b] - pos[a]), old_acc[b])
                            - 4 * inner_1 - inner_2))

        for a in range(len(mas)):
            for b in range(len(mas)):
                if a == b:
                    continue

                acc[a] += (1 / constants.c.value ** 2 * constants.G.value * mas[b] / np.linalg.norm(pos[b] - pos[a]) ** 2
                           * np.dot((pos[a] - pos[b]) / np.linalg.norm(pos[a] - pos[b]),
                                    4 * vel[a] - 3 * vel[b])
                           * (vel[a] - vel[b])
                           )

        for a in range(len(mas)):
            for b in range(len(mas)):
                if a == b:
                    continue

                acc[a] += (7 / 2 / constants.c.value ** 2 * constants.G.value * mas[b]
                           * old_acc[b] / np.linalg.norm(pos[b] - pos[a]))

        if np.allclose(old_acc, acc):
            break

        old_acc = acc

    out[:, 3:] = old_acc

    return out


