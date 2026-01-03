import inspect


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
    :param x: first integer value
    :param y: second integer value
    :param a: coefficient for x
    :param b: coefficient for y
    :param c: divisor
    :return: result of the equation
    """
  
    for name, value in {"x": x, "y": y, "a": a, "b": b, "c": c}.items():
        if not isinstance(value, int):
            raise TypeError(f"{name} must be int")

    return (x * a + y * b) / c


_fn_total_counter = 0
_fn_callers: dict[str, int] = {}


def fn_w_counter() -> (int, dict[str, int]):
    global _fn_total_counter, _fn_callers

    _fn_total_counter += 1

    caller_module = inspect.stack()[1].frame.f_globals.get("__name__", "__main__")

    _fn_callers[caller_module] = _fn_callers.get(caller_module, 0) + 1

    return _fn_total_counter, {caller_module: _fn_callers[caller_module]}
