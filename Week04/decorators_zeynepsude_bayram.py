import time
import tracemalloc


def performance(func):
    def wrapper(*args, **kwargs):
        performance.counter += 1
        tracemalloc.start()
        start = time.perf_counter()
        result = func(*args, **kwargs)
        performance.total_time += time.perf_counter() - start
        performance.total_mem += tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        return result
    return wrapper


performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
