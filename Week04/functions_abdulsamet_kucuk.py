custom_power = lambda x=0, /, e=1: x**e


def custom_equation(
    x: int = 0,
    y: int = 0,
    a: int = 1,
    b: int = 1,
    *,
    c: int = 1,
) -> float:
    """
    :param x: first value
    :param y: second value
    :param a: multiplier for x
    :param b: multiplier for y
    :param c: divisor
    :return: result of the equation
    """
    if not all(isinstance(v, int) for v in (x, y, a, b, c)):
        raise TypeError("all parameters must be int")
    return (a * x + b * y + x + y) / c


def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "_counter"):
        fn_w_counter._counter = 0
    fn_w_counter._counter += 1
    module_name = __name__.split(".")[-1]
    return fn_w_counter._counter, {module_name: fn_w_counter._counter}
