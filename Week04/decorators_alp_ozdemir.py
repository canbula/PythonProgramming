import functools
import time
import tracemalloc

def performance(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
       
        tracemalloc.start()
        start_time = time.perf_counter()
        
        try:
            
            result = func(*args, **kwargs)
        finally:
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            end_time = time.perf_counter()

           
            performance.counter += 1
            performance.total_time += (end_time - start_time)
            performance.total_mem += peak
            
        return result
    return wrapper


performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
