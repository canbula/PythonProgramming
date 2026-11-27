import time
import tracemalloc
from functools import wraps

def performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.counter += 1
        tracemalloc.start()
        t0 = time.perf_counter()
        
        try:
            # We use try/finally to ensure resources are calculated 
            # even if the function throws an error!
            return func(*args, **kwargs)
        finally:
            wrapper.total_time += time.perf_counter() - t0
            wrapper.total_mem += tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            
    # Unique trick: initialize all required attributes in a single line
    wrapper.__dict__.update(counter=0, total_time=0.0, total_mem=0)
    
    return wrapper
