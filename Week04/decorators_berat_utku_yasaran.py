import time
import tracemalloc

def performance(func):

    def wrapper(*args, **kwargs):

        tracemalloc.start()
        start = time.time()

        try:
            result = func(*args, **kwargs)

        finally:
            end = time.time()
            memory = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()

            performance.count += 1
            performance.total_time += end - start
            performance.total_memory += memory

        return result

    return wrapper


performance.count = 0
performance.total_time = 0
performance.total_memory = 0
