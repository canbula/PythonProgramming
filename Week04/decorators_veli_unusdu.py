import time, tracemalloc
from functools import wraps

def performance(func):
    performance.c = performance.c + 1 if hasattr(performance, "c") else 1
    performance.t = getattr(performance, "t", 0.0)
    performance.m = getattr(performance, "m", 0)

    @wraps(func)
    def wrapper(*a, **k):
        performance.c += 1
        t0 = time.perf_counter()
        tracemalloc.start()
        r = func(*a, **k)
        performance.t += time.perf_counter() - t0
        performance.m += tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        return r
    return wrapper

performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
