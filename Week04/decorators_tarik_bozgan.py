import time
import tracemalloc

def performance(func):
    func.counter = 0
    func.total_time = 0
    func.total_mem = 0

    def wrapper(*args, **kwargs):
        func.counter += 1
        start_time = time.perf_counter()
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        func.total_time += (time.perf_counter() - start_time)
        func.total_mem += peak

        return result

    return wrapper
