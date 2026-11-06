import time
import tracemalloc
from functools import wraps


# Measure function performance
def performance(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        start_time = time.perf_counter()

        was_tracing = tracemalloc.is_tracing()

        if not was_tracing:
            tracemalloc.start()

        start_memory, _ = tracemalloc.get_traced_memory()

        try:
            result = func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()

            _, peak_memory = tracemalloc.get_traced_memory()

            wrapper.counter += 1
            wrapper.total_time += end_time - start_time
            wrapper.total_mem += max(
                0, peak_memory - start_memory
            )

            if not was_tracing:
                tracemalloc.stop()

        return result

    wrapper.counter = 0
    wrapper.total_time = 0.0
    wrapper.total_mem = 0

    return wrapper