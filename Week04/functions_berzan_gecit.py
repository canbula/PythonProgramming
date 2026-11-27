custom_power = lambda x=0, /, e=1: x**e


def custom_equation(
    x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1
) -> float:
    """
    Calculates (x**a + y**b) / c.

    :param x: first base (positional-only)
    :param y: second base (positional-only)
    :param a: exponent of x
    :param b: exponent of y
    :param c: divisor (keyword-only)
    :return: the result of (x**a + y**b) / c
    """
    if not all(isinstance(v, int) for v in (x, y, a, b, c)):
        raise TypeError("All arguments must be integers")
    return (x**a + y**b) / c


def fn_w_counter() -> (int, dict[str, int]):

    fn_w_counter.calls += 1
    fn_w_counter.callers[__name__] = fn_w_counter.callers.get(__name__, 0) + 1
    return fn_w_counter.calls, dict(fn_w_counter.callers)


fn_w_counter.calls = 0
fn_w_counter.callers = {}
