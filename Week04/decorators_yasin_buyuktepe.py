import time
import tracemalloc


def performance(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            performance.counter += 1
            performance.total_time += elapsed
            performance.total_mem += peak
    return wrapper


performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
