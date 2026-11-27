import time
import tracemalloc

def performance(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        initial =time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        performance.counter +=1
        performance.total_time +=end-initial
        performance.total_mem += peak

        return result
    return wrapper

performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
