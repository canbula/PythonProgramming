import time
import tracemalloc


def performance(fn):
    counter = 0
    total_time = 0
    total_mem = 0

    def wrapper(*args, **kwargs):
        nonlocal counter, total_time, total_mem

        counter += 1

        tracemalloc.start()
        start_mem, _ = tracemalloc.get_traced_memory()

        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()

        end_mem, _ = tracemalloc.get_traced_memory()

        total_time += (end - start)
        total_mem += (end_mem - start_mem)

        tracemalloc.stop()

        wrapper.counter = counter
        wrapper.total_time = total_time
        wrapper.total_mem = total_mem

        return result

    wrapper.counter = counter
    wrapper.total_time = total_time
    wrapper.total_mem = total_mem

    return wrapper
