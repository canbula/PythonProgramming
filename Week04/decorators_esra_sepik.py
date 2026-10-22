import time
import tracemalloc


def performance(fn):
    """
    Decorator that measures the execution time and memory usage of a function.
    Statistics are kept in performance.counter, performance.total_time
    and performance.total_mem.
    """
    def _inner(*args, **kwargs):
        tracemalloc.start()
        begin = time.time()
        output = fn(*args, **kwargs)
        end = time.time()
        used = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()

        setattr(performance, "counter", getattr(performance, "counter", 0) + 1)
        setattr(performance, "total_time", getattr(performance, "total_time", 0) + (end - begin))
        setattr(performance, "total_mem", getattr(performance, "total_mem", 0) + used)
        return output

    _inner.__name__ = fn.__name__
    _inner.__doc__ = fn.__doc__
    return _inner


performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
