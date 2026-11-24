import time
import tracemalloc


def performance(fn):
    def _performance(*args, **kwargs):
        if not hasattr(performance, "counter"):
            performance.counter = 0
            performance.total_time = 0
            performance.total_mem = 0

        tracemalloc.start()
        t0 = time.perf_counter()
        res = fn(*args, **kwargs)
        t1 = time.perf_counter()
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        performance.counter += 1
        performance.total_time += t1 - t0
        performance.total_mem += peak_memory
        return res

    return _performance


performance.counter = 0
performance.total_time = 0
performance.total_mem = 0