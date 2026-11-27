import functools
import time
import tracemalloc


def performance(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        performance.counter += 1
        was_tracing = tracemalloc.is_tracing()
        if not was_tracing:
            tracemalloc.start()
        tracemalloc.reset_peak()
        start_mem = tracemalloc.get_traced_memory()[0]
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            performance.total_time += time.perf_counter() - start
            peak = tracemalloc.get_traced_memory()[1]
            performance.total_mem += max(0, peak - start_mem)
            if not was_tracing:
                tracemalloc.stop()

    return wrapper


performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
