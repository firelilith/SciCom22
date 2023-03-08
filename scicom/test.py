from scicom.post_newton_eih.nbody import _diff_eq
import numpy as np

x = np.array([[1, 0, 0, 0, 0.5, 0],
              [-1, 0, 0, 0, -0.5, 0]])
m = np.array([1, 1]) * 10 ** 17

print(_diff_eq(m, x))

