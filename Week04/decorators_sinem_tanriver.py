import time
import tracemalloc


def performance(func):
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

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


performance.counter = 0
performance.total_time = 0
performance.total_mem = 0

performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
