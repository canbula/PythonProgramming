custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates the result of the equation (x**a + y**b) / c.

    :param x: The first base, positional-only
    :type x: int
    :param y: The second base, positional-only
    :type y: int
    :param a: The exponent of x, positional-or-keyword
    :type a: int
    :param b: The exponent of y, positional-or-keyword
    :type b: int
    :param c: The divisor, keyword-only
    :type c: int
    :raises TypeError: If any of the arguments is not an integer
    :return: The result of (x**a + y**b) / c
    :rtype: float
    """
    for name, value in (("x", x), ("y", y), ("a", a), ("b", b), ("c", c)):
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
    return (x ** a + y ** b) / c


def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "total_calls"):
        fn_w_counter.total_calls = 0
        fn_w_counter.callers = {}
    caller = __name__
    fn_w_counter.total_calls += 1
    fn_w_counter.callers[caller] = fn_w_counter.callers.get(caller, 0) + 1
    return fn_w_counter.total_calls, fn_w_counter.callers
