from scicom.post_newton_eih.nbody import _diff_eq
import numpy as np
from astropy import units, constants
from scicom.library import *

m = np.array([1, 2, 0, 0])*10**22
x = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
v = np.array([[1, 0, 0], [-1, 0, 0], [0, 2, -2], [0, -2, 2]])


def test_this_shit(mas, pos, vel, iterations=5):

    old_acc = np.zeros(pos.shape)

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
                        np.dot(v[a], v[a]) + 2 * np.dot(v[b], v[b]) - 4 * np.dot(v[a], v[b])
                        + 3/2 * np.dot((pos[b] - pos[a]) / np.linalg.norm(pos[b] - pos[a]), v[b]) ** 2
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

    return acc


print(test_this_shit(m, x, v))

vals = np.concatenate((x, v), axis=1)

print(_diff_eq(m, vals)[:, 3:])
