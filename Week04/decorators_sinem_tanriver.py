import time
import tracemalloc
from functools import wraps


def performance(func):
    """Measures time and memory of the decorated function and keeps statistics."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        started_here = not tracemalloc.is_tracing()
        if started_here:
            tracemalloc.start()
        tracemalloc.reset_peak()
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        _, peak = tracemalloc.get_traced_memory()
        if started_here:
            tracemalloc.stop()

        performance.counter += 1
        performance.total_time += elapsed
        performance.total_mem += peak
        return result
    return wrapper


performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
