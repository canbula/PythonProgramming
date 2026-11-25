import time
import tracemalloc
from functools import wraps


def performance(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        tracemalloc.start()
        start_time = time.perf_counter()

        try:
            result = func(*args, **kwargs)
        finally:
            elapsed_time = time.perf_counter() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            performance.counter += 1
            performance.total_time += elapsed_time
            performance.total_mem += peak

        return result

    return wrapper


performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
