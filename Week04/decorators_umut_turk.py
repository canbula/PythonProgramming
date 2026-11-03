import time
import tracemalloc

def performance(f):
    def _performance(*args, **kwargs):
        if not hasattr(_performance, "counter"):
            _performance.counter = 0
        _performance.counter += 1 
        tracemalloc.start()
        x = time.time()
        f(args, kwargs)
        total_time = time.time() - x
        total_mem = tracemalloc.get_traced_memory
        tracemalloc.stop
    return _performance