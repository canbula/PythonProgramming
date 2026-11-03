import inspect


custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(
    x: int = 0,
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
    :return: The calculated result.
    :rtype: float
    """
    return float((x ** a + y ** b) / c)


def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "counts"):
        fn_w_counter.counts = {}

    frame = inspect.currentframe().f_back
    caller_name = frame.f_globals.get("__name__", "__main__")

    counts = fn_w_counter.counts
    counts[caller_name] = counts.get(caller_name, 0) + 1

    return sum(counts.values()), counts.copy()
