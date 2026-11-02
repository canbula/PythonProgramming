import functools
import time
import tracemalloc


def performance(fn):
    """
    This decorator measures the time and memory of the calls of a function.
    The statistics of all decorated functions are saved in its attributes.
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # shortcut: a decorated function calling another one under-reports
        # memory because tracemalloc is global, keep calls flat to stay exact
        tracemalloc.start()
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            performance.total_time += time.perf_counter() - start
            performance.total_mem += tracemalloc.get_traced_memory()[1]
            performance.counter += 1
            tracemalloc.stop()

    return wrapper


performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
