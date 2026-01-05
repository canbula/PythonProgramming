import time
import tracemalloc
from functools import update_wrapper


class performance:
    counter = 0
    total_time = 0.0
    total_mem = 0

    def __init__(self, fn):
        self.fn = fn
        update_wrapper(self, fn)

    def __call__(self, *args, **kwargs):
        tracemalloc.start()
        t0 = time.perf_counter()

        out = self.fn(*args, **kwargs)

        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        performance.counter += 1
        performance.total_time += (t1 - t0)
        performance.total_mem += peak

        return out
