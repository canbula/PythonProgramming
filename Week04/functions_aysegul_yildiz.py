import inspect


# custom_power
custom_power = lambda x=0, /, e=1: x**e


# custom_equation
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

    for name, value in {"x": x, "y": y, "a": a, "b": b, "c": c}.items():
        if not isinstance(value, int):
            raise TypeError(f"{name} must be int")

    return (x**a + y**b) / c


# fn_w_counter
_counter = 0
_callers = {}


def fn_w_counter() -> (int, dict[str, int]):
    global _counter  # ✅ sadece bu global gerekli

    _counter += 1

    module_name = inspect.getmodule(fn_w_counter).__name__
    _callers[module_name] = _callers.get(module_name, 0) + 1

    return _counter, {module_name: _callers[module_name]}
