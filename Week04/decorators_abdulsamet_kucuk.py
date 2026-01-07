import time
import sys

def performance(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        performance.counter += 1
        performance.total_time += end - start

        try:
            performance.total_mem += sys.getsizeof(result)
        except Exception:
            pass

        return result

    return wrapper

performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
