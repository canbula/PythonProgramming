import time
import tracemalloc
from functools import wraps


def performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        end_time = time.time()

        performance.counter += 1
        performance.total_time += (end_time - start_time)
        performance.total_mem += peak

        return result

    return wrapper


# decorator attributes
performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
