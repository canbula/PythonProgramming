custom_power = lambda x=0, /, e=1: x**e

def custom_equation(
        x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:

    """
    Function calculates (x**a + y**b) / c.

    :param x: base value for first term (positional-only).
    :type x: int
    :param y: base value for second term (positional-only).
    :type y: int
    :param a: exponent for x (positional-or-keyword).
    :type a: int
    :param b: exponent for y (positional-or-keyword).
    :type b: int
    :param c: divisor value (keyword-only).
    :type c: int
    :return: result of (x**a + y**b) / c
    :rtype: float
    """

    return (x ** a + y ** b) / c

def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "callers"):
        fn_w_counter.callers = {}

    fn_w_counter.callers[__name__] = fn_w_counter.callers.get(__name__, 0) + 1

    return sum(fn_w_counter.callers.values()), dict(fn_w_counter.callers)
