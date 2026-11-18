import time
import tracemalloc


def performance(func):
    def _performance(*args, **kwargs):
        tracemalloc.start()
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        performance.counter += 1
        performance.total_time += end - start
        performance.total_mem += peak
        return result
    return _performance


performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
