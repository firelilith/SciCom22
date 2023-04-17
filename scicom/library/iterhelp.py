import logging

logger = logging.getLogger(__name__)


def split_generator(gen_that_yields_2):
    cache_1 = []
    cache_2 = []

    def gen1(x):
        while True:
            if len(cache_1) != 0:
                yield cache_1.pop(0)
            else:
                try:
                    x1, x2 = next(x)
                except StopIteration:
                    return
                cache_2.append(x2)
                yield x1

    def gen2(x):
        while True:
            if len(cache_2) != 0:
                yield cache_2.pop(0)
            else:
                try:
                    x1, x2 = next(x)
                except StopIteration:
                    return
                cache_1.append(x1)
                yield x2

    return gen1(gen_that_yields_2), gen2(gen_that_yields_2)


def sparsify(series, timestep):
    steps, times, masses, labels = series

    def gen(st, ti, dt):
        vals = zip(st, ti)

        last_time = 0

        for s, t in vals:
            if t - last_time >= dt:
                logger.debug(f"passed time {last_time}, writing")
                last_time += dt
                yield s, t

    return *split_generator(gen(steps, times, timestep)), masses, labels


def tail(series, n):
    steps, times, masses, labels = series

    out_steps = []
    out_times = []
    for i, val, t in zip(range(n), steps, times):
        out_steps.append(val)
        out_times.append(t)

    for val, t in zip(steps, times):
        out_steps.append(val)
        out_steps.pop(0)
        out_times.append(val)
        out_times.pop(0)

    return (i for i in out_steps), (i for i in out_times), masses, labels


def head(series, n):
    steps, times, masses, labels = series

    return ((val for val, i in list(zip(steps, range(n)))),
            (t for t, i in list(zip(times, range(n)))),
            masses,
            labels)
