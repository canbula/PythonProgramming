import time
import tracemalloc


# Decorator to measure time and memory of a function
def performance(func):
    def wrapper(*args, **kwargs):
        # Start tracking memory and time
        tracemalloc.start()
        start_time = time.perf_counter()

        # Run the original function
        result = func(*args, **kwargs)

        # Calculate passed time and peak memory
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()

        # Update counter, total time, and total memory
        performance.counter += 1
        performance.total_time += end_time - start_time
        performance.total_mem += peak

        # Stop tracking memory
        tracemalloc.stop()

        return result

    return wrapper


# Set default values to zero
performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
