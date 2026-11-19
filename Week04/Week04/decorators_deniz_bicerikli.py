import time
import tracemalloc

def performance(func):

    def wrapper(*args, **kwargs):
        
        tracemalloc.start()
        start = time.perf_counter()
        start_mem = tracemalloc.get_traced_memory()[0]
        tracemalloc.reset_peak()

        try:
            result = func(*args, **kwargs)
        
        finally:
            end = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            
            performance.counter += 1
            performance.total_time += end - start
            performance.total_mem += peak - start_mem
            
            tracemalloc.stop()

        return result
    return wrapper

performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
