import time
import tracemalloc
from functools import wraps


def performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        performance.counter += 1

        tracemalloc.start()
        start_time = time.perf_counter()

        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()

            performance.total_time += end_time - start_time
            performance.total_mem += peak

            tracemalloc.stop()

    return wrapper


performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
