import time
import tracemalloc
from functools import wraps


def performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        was_tracing = tracemalloc.is_tracing()
        if not was_tracing:
            tracemalloc.start()
        tracemalloc.reset_peak()
        start_mem = tracemalloc.get_traced_memory()[0]
        try:
            return func(*args, **kwargs)
        finally:
            peak = tracemalloc.get_traced_memory()[1]
            if not was_tracing:
                tracemalloc.stop()
            performance.counter += 1
            performance.total_mem += peak - start_mem
            performance.total_time += time.perf_counter() - start

    return wrapper


performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0