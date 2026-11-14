import functools
import time
import tracemalloc


def performance(fn):
    """
    Decorator that measures execution time and memory of the wrapped function.

    Statistics are stored as attributes on the decorator itself:

    - ``performance.counter``: number of decorated-function calls
    - ``performance.total_time``: total time spent in seconds
    - ``performance.total_mem``: total memory consumed in bytes

    :param fn: the function to decorate
    :type fn: callable
    :return: the wrapped function
    :rtype: callable
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        started_here = not tracemalloc.is_tracing()
        if started_here:
            tracemalloc.start()
        tracemalloc.reset_peak()
        mem_before = tracemalloc.get_traced_memory()[0]
        start = time.perf_counter()

        try:
            return fn(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            peak = tracemalloc.get_traced_memory()[1]
            if started_here:
                tracemalloc.stop()
            performance.counter += 1
            performance.total_time += elapsed
            performance.total_mem += max(peak - mem_before, 0)

    return wrapper


performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0