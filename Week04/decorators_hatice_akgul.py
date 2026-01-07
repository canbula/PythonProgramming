import time
import tracemalloc
import functools

def performance(func):
    """
    Fonksiyonun performansını ölçen ve istatistiklerini saklayan dekoratör.
    """
    if not hasattr(performance, "counter"):
        performance.counter = 0
        performance.total_time = 0.0
        performance.total_mem = 0

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
       
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
      
        performance.counter += 1
        performance.total_time += (end_time - start_time)
        performance.total_mem += peak_mem
        
        return result

    return wrapper

performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
