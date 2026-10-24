import time
import sys

def performance(fn):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = fn(*args, **kwargs)
        end_time = time.time()
        
        performance.counter += 1
        performance.total_time += (end_time - start_time)
        performance.total_mem += sys.getsizeof(result)
        
        return result

    return wrapper

performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0.0
