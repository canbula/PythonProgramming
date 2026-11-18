import time
import tracemalloc

def performance(func):

    def wrapper(*args, **kwargs):

        tracemalloc.start()
        start_time = time.perf_counter()
        start_mem = tracemalloc.get_traced_memory()[0]

        try:
            return func(*args, **kwargs)

        finally:
            end_time = time.perf_counter()
            peak_mem = tracemalloc.get_traced_memory()[1]

            performance.counter += 1
            performance.total_time += end_time - start_time
            performance.total_mem += max(peak_mem - start_mem, 0)

            tracemalloc.stop()

    for attr in ("__module__", "__name__", "__qualname__", "__doc__", "__annotations__", "__type_params__"):
        if hasattr(func, attr):
            setattr(wrapper, attr, getattr(func, attr))
    wrapper.__dict__.update(getattr(func, "__dict__", {}))
    wrapper.__wrapped__ = func

    return wrapper

performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
