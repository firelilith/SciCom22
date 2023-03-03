import numpy as np


def distance_vec(pos):
    return pos[..., :3] - pos[..., :3].reshape((-1, 1, 3))


def distance_sca(pos):
    dist = distance_vec(pos)
    return np.sqrt(np.sum(np.square(dist), axis=2))


def distance_unt(pos):
    dist = distance_vec(pos)
    scal = np.sqrt(np.sum(np.square(dist), axis=2))
    with np.errstate(divide="ignore", invalid="ignore"):
        out = dist / scal[:, :, None]
    out[~np.isfinite(out)] = 0
    return out
