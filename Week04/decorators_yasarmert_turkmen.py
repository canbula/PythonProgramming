import time
import tracemalloc


def performance(func):
  def wrapper(*args, **kwargs):
    performance.counter += 1
    start_time = time.perf_counter()
    tracemalloc.start()

    result = func(*args, **kwargs)

    current_mem, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.perf_counter()

    performance.total_time += end_time - start_time
    performance.total_mem += current_mem
    return result

  return wrapper


performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0