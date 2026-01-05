custom_power = lambda x=0, /, e=1: pow(x, e)

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
    Computes a custom mathematical equation.

    :param x: positional-only integer, default 0
    :param y: positional-only integer, default 0
    :param a: multiplier for x, default 1
    :param b: multiplier for y, default 1
    :param c: divisor value, keyword-only, default 1
    :return: calculated float result
    """

    for val in (x, y, a, b, c):
        if not isinstance(val, int):
            raise TypeError("Parameters must be integers")

    if c == 0:
        raise ZeroDivisionError("c must not be zero")

    return (a * x + b * y) / c

_counter = 0

def fn_w_counter() -> (int, dict[str, int]):
    global _counter
    _counter += 1

    module_name = __name__.split('.')[-1]
    return _counter, {module_name: _counter}
