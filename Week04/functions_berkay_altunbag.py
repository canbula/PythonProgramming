custom_power = lambda x=0, /, e=1: x**e


def custom_equation(
    x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1
) -> float:
    """
    Calculates (x**a + y**b) / c.

    :param x: base of the first term (positional-only)
    :param y: base of the second term (positional-only)
    :param a: exponent of x
    :param b: exponent of y
    :param c: divisor (keyword-only)
    :return: the result of (x**a + y**b) / c
    """
    for name, value in (("x", x), ("y", y), ("a", a), ("b", b), ("c", c)):
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an int")
    return (x**a + y**b) / c


_counter = 0


def fn_w_counter() -> (int, dict[str, int]):
    global _counter
    _counter += 1
    return _counter, {__name__: _counter}