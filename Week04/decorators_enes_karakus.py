import time
import tracemalloc
from functools import wraps


def performance(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not hasattr(performance, "counter"):
            performance.counter = 0
            performance.total_time = 0.0
            performance.total_mem = 0

        tracemalloc.start()
        t_start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - t_start
            _, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            performance.counter += 1
            performance.total_time += elapsed
            performance.total_mem += peak_mem

    return wrapper


performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0