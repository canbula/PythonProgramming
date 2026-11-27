custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Compute (x**a + y**b) / c.

    :param x: First base, positional-only
    :type x: int
    :param y: Second base, positional-only
    :type y: int
    :param a: Exponent of x
    :type a: int
    :param b: Exponent of y
    :type b: int
    :param c: Divisor, keyword-only
    :type c: int
    :return: The result of (x**a + y**b) / c
    :rtype: float
    """
    return (x ** a + y ** b) / c


def fn_w_counter() -> (int, dict[str, int]):
    fn_w_counter.total += 1
    fn_w_counter.callers[__name__] = fn_w_counter.callers.get(__name__, 0) + 1

    return fn_w_counter.total, dict(fn_w_counter.callers)


fn_w_counter.total = 0
fn_w_counter.callers = {}