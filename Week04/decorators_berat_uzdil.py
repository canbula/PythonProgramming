import time
import tracemalloc
from functools import wraps

def performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        performance.counter += 1

        tracemalloc.start()
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        elapsed_time = time.perf_counter() - start_time
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        performance.total_time += elapsed_time
        performance.total_mem += peak_mem

        return result

    return wrapper

performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0