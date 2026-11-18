
custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates (x**a + y**b) / c.

    :param x: First base, positional-only
    :param y: Second base, positional-only
    :param a: Exponent of x
    :param b: Exponent of y
    :param c: Divisor, keyword-only
    :return: Result of (x**a + y**b) / c
    """
    return (x ** a + y ** b) / c


_total_calls = 0
_callers = {}


def fn_w_counter() -> (int, dict[str, int]):
    global _total_calls
    caller = __name__
    _total_calls += 1
    _callers[caller] = _callers.get(caller, 0) + 1
    return _total_calls, _callers
