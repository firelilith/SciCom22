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

