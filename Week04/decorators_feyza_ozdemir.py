import functools
import time
import tracemalloc


def performance(func):
    """
    A decorator that measures execution time, memory usage, and call count
    across all decorated functions.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        already_tracing = tracemalloc.is_tracing()
        if not already_tracing:
            tracemalloc.start()
        tracemalloc.reset_peak()

        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_time = time.perf_counter() - start_time

        _, peak_mem = tracemalloc.get_traced_memory()

        if not already_tracing:
            tracemalloc.stop()

        performance.counter += 1
        performance.total_time += elapsed_time
        performance.total_mem += peak_mem

        return result

    return wrapper


performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0