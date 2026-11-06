import time
import tracemalloc


def performance(func):
    """
    Measure the performance of the decorated function.

    The decorator keeps three statistics as its own attributes:
    counter (number of calls), total_time (in seconds) and
    total_mem (peak memory in bytes used by the calls).
    """
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start_time
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            performance.counter += 1
            performance.total_time += elapsed
            performance.total_mem += peak
        return result

    return wrapper


performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
