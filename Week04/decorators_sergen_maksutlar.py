import time
import tracemalloc


def monitor(func):

    def execute(*args, **kwargs):

        tracemalloc.start()

        initial_time = time.perf_counter()
        initial_memory = tracemalloc.get_traced_memory()[0]

        tracemalloc.reset_peak()

        try:
            output = func(*args, **kwargs)

        finally:
            elapsed_time = time.perf_counter() - initial_time
            used_memory, max_memory = tracemalloc.get_traced_memory()

            monitor.calls += 1
            monitor.duration += elapsed_time
            monitor.memory_usage += max_memory - initial_memory

            tracemalloc.stop()

        return output

    return execute


monitor.calls = 0
monitor.duration = 0
monitor.memory_usage = 0
