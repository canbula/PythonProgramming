import inspect

# x is positional-only (default 0), e is positional-or-keyword (default 1)
custom_power = lambda x=0, /, e=1: x**e


def custom_equation(
    x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1
) -> float:
    """
    Calculate (x**a + y**b) / c.

    :param x: Positional-only base of the first term.
    :type x: int
    :param y: Positional-only base of the second term.
    :type y: int
    :param a: Exponent applied to x.
    :type a: int
    :param b: Exponent applied to y.
    :type b: int
    :param c: Keyword-only divisor.
    :type c: int
    :return: The value of (x**a + y**b) / c.
    :rtype: float
    """
    return (x**a + y**b) / c


_total_calls: int = 0
_calls_by_caller: dict[str, int] = {}


def fn_w_counter() -> (int, dict[str, int]):
    """
    Count how many times this function has been called, and by whom.

    :return: A tuple of the total number of calls and a dictionary mapping
        each caller's ``__name__`` to the number of calls it made.
    :rtype: tuple[int, dict[str, int]]
    """
    global _total_calls
    caller = inspect.currentframe().f_back.f_globals["__name__"]
    _total_calls += 1
    _calls_by_caller[caller] = _calls_by_caller.get(caller, 0) + 1
    return _total_calls, dict(_calls_by_caller)


if __name__ == "__main__":
    assert custom_power(2) == 2
    assert custom_power(2, 3) == 8
    assert custom_power(2, e=2) == 4

    assert custom_equation(2, 3) == 5.0
    assert custom_equation(2, 3, 2) == 7.0
    assert custom_equation(2, 3, 2, 3) == 31.0
    assert custom_equation(3, 5, a=2, b=3, c=4) == 33.5
    assert custom_equation(3, 5, 2, b=3, c=4) == 33.5
    assert custom_equation(3, 5, 2, 3, c=4) == 33.5

    for i in range(10):
        fn_w_counter()
    assert fn_w_counter() == (11, {"__main__": 11})
