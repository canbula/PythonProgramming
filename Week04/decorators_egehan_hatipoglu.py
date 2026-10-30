import time
import tracemalloc

def performance(func):

    def wrapper(*args, **kwargs):

        wrapper.counter += 1

        tracemalloc.start()

        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        current, peak = tracemalloc.get_traced_memory()

        wrapper.total_time += end - start
        wrapper.total_mem += peak

        tracemalloc.stop()

        return result

    wrapper.counter = 0
    wrapper.total_time = 0
    wrapper.total_mem = 0

    return wrapper


@performance
def my_function():
    total = 0
    for i in range(1000):
        total += i


my_function()
my_function()
my_function()

print("Counter:", my_function.counter)
print("Total Time:", my_function.total_time)
print("Total Memory:", my_function.total_mem)
