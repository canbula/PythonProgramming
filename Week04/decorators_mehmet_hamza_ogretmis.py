import time
import tracemalloc


def performance(func):
    """Measure the time and memory each call of func takes and keep running totals."""

    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start = time.perf_counter()

        result = func(*args, **kwargs)

        elapsed = time.perf_counter() - start
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