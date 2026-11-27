import time
import tracemalloc


def performance(fn):
    """
    Measures the execution time and memory usage of a function.
    """

    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = time.perf_counter()

        try:
            result = fn(*args, **kwargs)
        finally:
            elapsed_time = time.perf_counter() - start_time
            memory_used = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()

            performance.counter += 1
            performance.total_time += elapsed_time
            performance.total_mem += memory_used

        return result

    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__

    return wrapper


performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
