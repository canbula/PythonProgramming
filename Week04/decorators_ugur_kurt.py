import time
import tracemalloc


class performance:
    counter = 0
    total_time = 0.0
    total_mem = 0

    def __init__(self, func):
        self.func = func
        # Replaces functools.wraps(func)(self)
        for attr in ("__module__", "__name__", "__qualname__", "__doc__"):
            try:
                setattr(self, attr, getattr(func, attr))
            except AttributeError:
                pass
        self.__dict__.update(getattr(func, "__dict__", {}))
        self.__wrapped__ = func

    def __call__(self, *args, **kwargs):
        performance.counter += 1

        tracemalloc.start()
        start = time.perf_counter()
        try:
            result = self.func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            performance.total_time += elapsed
            performance.total_mem += peak

        return result
            performance.total_time += elapsed
            performance.total_mem += peak

        return result
