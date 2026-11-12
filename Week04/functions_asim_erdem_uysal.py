custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates the result of (x**a + y**b) / c.

    :param x: First base, positional-only (default 0)
    :param y: Second base, positional-only (default 0)
    :param a: Exponent of x (default 1)
    :param b: Exponent of y (default 1)
    :param c: Divisor, keyword-only (default 1)
    :return: The result as a float
    """
    return (x ** a + y ** b) / c


def fn_w_counter() -> (int, dict[str, int]):
    """Counts the total number of calls and the number of calls per caller."""
    if not hasattr(fn_w_counter, "total"):
        fn_w_counter.total = 0
        fn_w_counter.callers = {}
    fn_w_counter.total += 1
    fn_w_counter.callers[__name__] = fn_w_counter.callers.get(__name__, 0) + 1
    return fn_w_counter.total, fn_w_counter.callers
