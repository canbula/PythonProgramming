import time
import tracemalloc

def performance(f):
    def _performance():
        if not hasattr(_performance, "counter"):
            counter = 0
        _performance.counter += 1 
        x = time.time()
        tracemalloc.start()
        f()
        total_mem = tracemalloc.get_traced_memory
        total_time = time.time() - x
        tracemalloc.stop