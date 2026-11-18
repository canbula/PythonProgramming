custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates an equation using the given integers.

    The formula is ``(x ** a + y ** b) / c``.

    :param x: positional-only value, defaults to 0
    :type x: int
    :param y: positional-only value, defaults to 0
    :type y: int
    :param a: exponent for x, defaults to 1
    :type a: int
    :param b: exponent for y, defaults to 1
    :type b: int
    :param c: keyword-only divisor, defaults to 1
    :type c: int
    :returns: the result of the equation
    :rtype: float
    """
    numerator = pow(x, a) + pow(y, b)
    return numerator / c


_call_count = 0
_caller_counts: dict[str, int] = {}


def fn_w_counter() -> (int, dict[str, int]):
    global _call_count
    caller_name = globals()["__name__"]
    _call_count += 1
    _caller_counts[caller_name] = _caller_counts.setdefault(caller_name, 0) + 1
    return (_call_count, dict(_caller_counts))
