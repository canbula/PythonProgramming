custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates the result of the equation (x**a + y**b) / c.

    :param x: First base, positional-only
    :param y: Second base, positional-only
    :param a: Exponent of x
    :param b: Exponent of y
    :param c: Divisor, keyword-only
    :return: Result of (x**a + y**b) / c as a float
    """
    for name, value in (("x", x), ("y", y), ("a", a), ("b", b), ("c", c)):
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
    return (x ** a + y ** b) / c


def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "total"):
        fn_w_counter.total = 0
        fn_w_counter.callers = {}
    fn_w_counter.total += 1
    fn_w_counter.callers[__name__] = fn_w_counter.callers.get(__name__, 0) + 1
    return fn_w_counter.total, fn_w_counter.callers
