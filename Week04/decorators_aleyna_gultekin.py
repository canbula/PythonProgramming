import time
import tracemalloc
import functools


class performance:
    """Decorator class collecting performance statistics of functions."""
    counter = 0
    total_time = 0.0
    total_mem = 0

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        was_tracing = tracemalloc.is_tracing()
        if not was_tracing:
            tracemalloc.start()
        mem_before = tracemalloc.get_traced_memory()[0]
        t0 = time.perf_counter()
        try:
            return self.func(*args, **kwargs)
        finally:
            t1 = time.perf_counter()
            mem_after, peak = tracemalloc.get_traced_memory()
            if not was_tracing:
                tracemalloc.stop()
            performance.counter += 1
            performance.total_time += t1 - t0
            performance.total_mem += max(peak - mem_before, 0)
