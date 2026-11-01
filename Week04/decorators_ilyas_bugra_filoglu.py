import time
import tracemalloc
from functools import wraps

tracemalloc.start()

def performance(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        performance.counter += 1

        tracemalloc.reset_peak()
        start_time = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start_time

        performance.total_time += elapsed

        _, peak_memory = tracemalloc.get_traced_memory()
        performance.total_mem += peak_memory

        return result

    return wrapper

performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
