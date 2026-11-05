
import time
import tracemalloc
from functools import wraps


def performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start = time.perf_counter()

        try:
            result = func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            peak_memory = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()

            performance.counter += 1
            performance.total_time += elapsed
            performance.total_mem += peak_memory

        return result

    return wrapper


performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
