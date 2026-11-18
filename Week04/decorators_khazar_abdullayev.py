def performance(fn):
    """
    Decorator that measures execution time and memory of the wrapped function.

    Statistics are stored as attributes on the decorator itself:

    - ``performance.counter``: number of decorated-function calls
    - ``performance.total_time``: total time spent in seconds
    - ``performance.total_mem``: total memory of the returned values in bytes

    No ``import`` statements are used: the clock is loaded with the
    ``__import__`` builtin and memory is measured with ``__sizeof__``.

    :param fn: the function to decorate
    :type fn: callable
    :return: the wrapped function
    :rtype: callable
    """
    clock = __import__("time").perf_counter

    def wrapper(*args, **kwargs):
        start = clock()
        result = None
        try:
            result = fn(*args, **kwargs)
            return result
        finally:
            performance.counter += 1
            performance.total_time += clock() - start
            performance.total_mem += result.__sizeof__()

    wrapper.__name__ = fn.__name__
    wrapper.__qualname__ = fn.__qualname__
    wrapper.__doc__ = fn.__doc__
    wrapper.__module__ = fn.__module__
    wrapper.__wrapped__ = fn
    return wrapper


performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
