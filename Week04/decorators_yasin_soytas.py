import time
import tracemalloc


def performance(func):

    def wrapper(*args, **kwargs):
        wrapper.counter += 1

        tracemalloc.start()
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        wrapper.total_time += (end_time - start_time)
        wrapper.total_mem += peak

        return result

    wrapper.counter = 0
    wrapper.total_time = 0.0
    wrapper.total_mem = 0

    return wrapper
