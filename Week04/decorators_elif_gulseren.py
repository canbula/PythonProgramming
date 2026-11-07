import time
import tracemalloc
from functools import wraps

def performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        performance.counter += 1
        
        tracemalloc.start()
        start_mem, _ = tracemalloc.get_traced_memory()
        
        start_time = time.perf_counter()
        
        result = func(*args, **kwargs)
        
        end_time = time.perf_counter()
        
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        time_taken = end_time - start_time
        mem_used = peak_mem - start_mem
        
        performance.total_time += time_taken
        performance.total_mem += mem_used
        
        return result

    return wrapper

performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
