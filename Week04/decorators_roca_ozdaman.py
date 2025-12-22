import time
import tracemalloc

def performance(func):
    if not hasattr(performance, "counter"):
        performance.counter = 0
        performance.total_time = 0.0
        performance.total_mem = 0

    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        tracemalloc.start()

        result = func(*args, **kwargs)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time = time.perf_counter()

        performance.counter += 1
        performance.total_time += (end_time - start_time)
        performance.total_mem += peak

        return result

    return wrapper
