import time
import tracemalloc
from functools import wraps


def performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if not tracemalloc.is_tracing():
            tracemalloc.start()

        tracemalloc.reset_peak()
        before = tracemalloc.get_traced_memory()[0]

        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()

        current, peak = tracemalloc.get_traced_memory()

        wrapper.counter += 1
        wrapper.total_time += end_time - start_time
        wrapper.total_mem += max(0, peak - before)

        return result

    wrapper.counter = 0
    wrapper.total_time = 0.0
    wrapper.total_mem = 0

    return wrapper


# Example function
@performance
def calculate():
    numbers = [i for i in range(1000)]
    return sum(numbers)


print(calculate())
print("Counter:", calculate.counter)
print("Total time:", calculate.total_time)
print("Total memory:", calculate.total_mem)
