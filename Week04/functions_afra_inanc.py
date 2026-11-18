custom_power = lambda x=0, /, e=1: x**e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates the equation (x**a + y**b) / c.

    :param x: The base of the first term, positional-only
    :type x: int
    :param y: The base of the second term, positional-only
    :type y: int
    :param a: The exponent of the first term
    :type a: int
    :param b: The exponent of the second term
    :type b: int
    :param c: The divisor, keyword-only
    :type c: int
    :return: The result of (x**a + y**b) / c

    """

    return (x**a + y**b) / c


_total_calls = 0
_calls_by_caller = {}


def fn_w_counter() -> (int, dict[str, int]):
    
    global _total_calls
    _total_calls += 1
    _calls_by_caller[__name__] = _calls_by_caller.get(__name__, 0) + 1
    return _total_calls, dict(_calls_by_caller)
