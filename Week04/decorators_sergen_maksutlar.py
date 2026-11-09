import time
import tracemalloc

def performance(f):
    if not hasattr(performance, "counter"):
        performance.counter = 0
        
    if not hasattr(performance, "total_time"):
        performance.total_time = 0.0
        
    if not hasattr(performance, "total_mem"):
        performance.total_mem = 0
        
    def _performance(*args, **kwargs):
        performance.counter += 1 
        
        tracemalloc.start()
        
        x = time.time()
        
        ret = f(*args, **kwargs)
        performance.total_time += time.time() - x
        performance.total_mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        return ret
    return _performance
