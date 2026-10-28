"""Week04 - Introduction to Python: functions."""

import sys

# x positional-only (default 0), e positional-or-keyword (default 1)
custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(
    x: int = 0,
    y: int = 0,
    /,
    a: int = 1,
    b: int = 1,
    *,
    c: int = 1,
) -> float:
    """
    Calculate (x**a + y**b) / c.

    :param x: first base (positional-only)
    :type x: int
    :param y: second base (positional-only)
    :type y: int
    :param a: exponent of x (positional-or-keyword)
    :type a: int
    :param b: exponent of y (positional-or-keyword)
    :type b: int
    :param c: divisor (keyword-only)
    :type c: int
    :return: the value of (x**a + y**b) / c
    :rtype: float
    """
    return (x ** a + y ** b) / c


_call_counts: dict[str, int] = {}
_total_calls: int = 0


def fn_w_counter() -> tuple[int, dict[str, int]]:
    """
    Count the calls made to this function together with caller information.

    :return: total number of calls and a dictionary mapping each caller's
        ``__name__`` to the number of calls made from that caller
    :rtype: tuple[int, dict[str, int]]
    """
    global _total_calls
    caller = sys._getframe(1).f_globals.get("__name__", "<unknown>")
    _total_calls += 1
    _call_counts[caller] = _call_counts.get(caller, 0) + 1
    return _total_calls, dict(_call_counts)


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
    assert fn_w_counter() == (11, {'__main__': 11})
    print("All examples passed.")
