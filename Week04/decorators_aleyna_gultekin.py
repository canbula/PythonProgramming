import time
import tracemalloc


def performance(fn):
    """
    Decorator that measures the execution time and memory usage of a function.
    Statistics are kept in performance.counter, performance.total_time
    and performance.total_mem.
    """
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        begin = time.time()
        try:
            output = fn(*args, **kwargs)
        finally:
            end = time.time()
            used = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            performance.counter += 1
            performance.total_time += end - begin
            performance.total_mem += used
        return output

    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper


performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
