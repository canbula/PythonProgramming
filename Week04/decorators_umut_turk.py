import time
import tracemalloc

def performance(f):
    def _performance(*args, **kwargs):
        if not hasattr(_performance, "counter"):
            counter = 0
        _performance.counter += 1 
        x = time.time()
        tracemalloc.start()
        f(args, kwargs)
        total_mem = tracemalloc.get_traced_memory
        total_time = time.time() - x
        tracemalloc.stop
    return _performance