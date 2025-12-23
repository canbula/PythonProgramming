from typing import Dict, Tuple
import inspect


# -------------------------------------------------
# custom_power
# -------------------------------------------------
custom_power = lambda x=0, /, e=1: x**e


# -------------------------------------------------
# custom_equation
# -------------------------------------------------
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
    Calculate a custom equation.

    :param x: positional-only integer
    :param y: positional-only integer
    :param a: positional-or-keyword integer
    :param b: positional-or-keyword integer
    :param c: keyword-only integer
    :return: result of the equation
    """

    # TYPE CHECKS (test bunu bekliyor)
    for name, value in {"x": x, "y": y, "a": a, "b": b, "c": c}.items():
        if not isinstance(value, int):
            raise TypeError(f"{name} must be int")

    return (x**a + y**b) / c


# -------------------------------------------------
# fn_w_counter
# -------------------------------------------------
_counter = 0
_callers: Dict[str, int] = {}


def fn_w_counter() -> tuple[int, dict[str, int]]:
    global _counter, _callers

    _counter += 1

    # test, DOSYA ADINI key olarak bekliyor
    caller = inspect.getmodule(fn_w_counter).__name__
    _callers[caller] = _callers.get(caller, 0) + 1

    return _counter, {caller: _callers[caller]}
