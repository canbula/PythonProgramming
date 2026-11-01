"""Week 04: Decorators homework."""

import functools
import time
import tracemalloc


def performance(func):
    """Track cumulative calls, elapsed time and peak memory allocation."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tracing_started_here = not tracemalloc.is_tracing()
        if tracing_started_here:
            tracemalloc.start()
        before_current, before_peak = tracemalloc.get_traced_memory()
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            current, peak = tracemalloc.get_traced_memory()
            allocated = max(0, peak - before_current)
            performance.counter += 1
            performance.total_time += elapsed
            performance.total_mem += allocated
            if tracing_started_here:
                tracemalloc.stop()

    return wrapper


performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
