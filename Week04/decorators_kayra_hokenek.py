import functools
import time
import tracemalloc

def performance(fn):

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        wrapper.counter += 1
        tracemalloc.start()
        start = time.perf_counter()

        try:
            result = fn(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            wrapper.total_time += elapsed
            wrapper.total_mem += peak

        return result

    wrapper.counter = 0
    wrapper.total_time = 0.0
    wrapper.total_mem = 0

    return wrapper
