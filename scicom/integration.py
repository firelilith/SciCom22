import numpy as np

def rk4_step(funcs, timestep, vals):
    k1 = np.zeros(shape=vals.shape)
    k2 = np.zeros(shape=vals.shape)
    k3 = np.zeros(shape=vals.shape)
    k4 = np.zeros(shape=vals.shape)

    for i, f in enumerate(funcs):
        print(k1)
        k1[:, i] = f(0, vals)
        k2[:, i] = f(timestep/2, vals + timestep/2 * k1)
        k3[:, i] = f(timestep/2, vals + timestep/2 * k2)
        k4[:, i] = f(timestep, vals + timestep * k3)

    return vals + timestep*(k1 + 2*k2 + 2*k3 + k4)/6