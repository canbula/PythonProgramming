import time
import tracemalloc
from functools import wraps


class performance:
    

    counter = 0        
    total_time = 0.0  
    total_mem = 0      

    def __init__(self, func):
        self.func = func
        wraps(func)(self)

    def __call__(self, *args, **kwargs):
        performance.counter += 1

        tracemalloc.start()
        start = time.perf_counter()
        try:
            result = self.func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            performance.total_time += elapsed
            performance.total_mem += peak

        return result
