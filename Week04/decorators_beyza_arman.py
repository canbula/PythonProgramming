from functools import wraps
from time import perf_counter
import tracemalloc


def performance(function):
    """Measure calls, elapsed time and peak traced memory."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        owns_tracing = not tracemalloc.is_tracing()
        if owns_tracing:
            tracemalloc.start()
        before, _ = tracemalloc.get_traced_memory()
        start = perf_counter()
        try:
            return function(*args, **kwargs)
        finally:
            performance.counter += 1
            performance.total_time += perf_counter() - start
            _, peak = tracemalloc.get_traced_memory()
            performance.total_mem += max(0, peak - before)
            if owns_tracing:
                tracemalloc.stop()
    return wrapper


performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
