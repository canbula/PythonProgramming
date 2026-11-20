import time
import tracemalloc
from functools import wraps


def fn_w_counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.counter += 1

        caller = func.__globals__.get("__name__", "__main__")
        wrapper.callers[caller] = wrapper.callers.get(caller, 0) + 1

        result = func(*args, **kwargs)
        return result

    wrapper.counter = 0
    wrapper.callers = {}
    return wrapper


def performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        tracemalloc.start()
        result = func(*args, **kwargs)
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        elapsed_time = time.perf_counter() - start_time

        wrapper.counter += 1
        wrapper.total_time += elapsed_time
        wrapper.total_mem += peak_mem

        return result

    wrapper.counter = 0
    wrapper.total_time = 0.0
    wrapper.total_mem = 0

    return wrapper
