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
    Calculate (x**a + y**b) / c.

    :param x: First base.
    :type x: int
    :param y: Second base.
    :type y: int
    :param a: First exponent.
    :type a: int
    :param b: Second exponent.
    :type b: int
    :param c: Divisor.
    :type c: int
    :return: The calculated result.
    :rtype: float
    """
    return (x ** a + y ** b) / c


_total_calls = 0
_calls_by_caller = {}


def fn_w_counter() -> tuple:
    global _total_calls

    _total_calls += 1
    caller = __name__

    _calls_by_caller[caller] = _calls_by_caller.get(caller, 0) + 1

    return _total_calls, dict(_calls_by_caller)
