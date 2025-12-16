import tracemalloc
import time
from functools import wraps

def performance(f):
    @wraps(f) 
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = time.time()
        
        result = f(*args, **kwargs)
        
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        wrapper.counter += 1
        wrapper.total_mem += peak
        wrapper.total_time += (end_time - start_time)
        
        return result

    wrapper.counter = 0
    wrapper.total_mem = 0
    wrapper.total_time = 0

    return wrapper
