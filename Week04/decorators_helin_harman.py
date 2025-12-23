import time
import tracemalloc
from functools import wraps


def performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        performance.counter += 1

        start_time = time.perf_counter()
        tracemalloc.start()

        result = func(*args, **kwargs)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time = time.perf_counter()

        performance.total_time += end_time - start_time
        performance.total_mem += peak

        return result

    return wrapper


# decorator attribute'ları (TESTLER BUNU BEKLİYOR)
performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
