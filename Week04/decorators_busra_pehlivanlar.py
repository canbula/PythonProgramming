import time
import sys

def performance(func):
    def wrapper(*args, **kwargs):
        start_t = time.perf_counter()
        
        result = func(*args, **kwargs)
        
        end_t = time.perf_counter()
        
        performance.counter += 1
        performance.total_time += (end_t - start_t)
        performance.total_mem += sys.getsizeof(result)
        
        return result
    return wrapper

performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
