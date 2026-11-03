import inspect


custom_power = lambda x=0, e=1, /: x ** e


def custom_equation(
    x: int,
    y: int = 0,
    /,
    a: int = 1,
    b: int = 1,
    *,
    c: int = 1
) -> float:
    """
    Calculate the result of the equation.

    :param x: First integer.
    :param y: Second integer.
    :param a: Exponent of x.
    :param b: Exponent of y.
    :param c: Divisor.
    :return: Result of the equation.
    :rtype: float
    """
    return float((x ** a + y ** b) / c)


def fn_w_counter():
    if not hasattr(fn_w_counter, "counts"):
        fn_w_counter.counts = {}

    caller = inspect.currentframe().f_back
    caller_name = caller.f_code.co_name

    counts = fn_w_counter.counts
    counts[caller_name] = counts.get(caller_name, 0) + 1

    return sum(counts.values()), counts.copy()
