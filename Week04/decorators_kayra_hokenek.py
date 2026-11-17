import functools
import time
import tracemalloc

def performance(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        performance.counter += 1
        tracemalloc.start()
        start = time.perf_counter()

        try:
            result = fn(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            performance.total_time += elapsed
            performance.total_mem += peak

        return result

    return wrapper
    
performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
