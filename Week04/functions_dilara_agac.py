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
    Custom equation function.

    :param x: first value
    :param y: second value
    :param a: power of x
    :param b: power of y
    :param c: divisor
    :return: result of equation
    """
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("x and y must be integers")
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int):
        raise TypeError("a, b and c must be integers")

    return (x ** a + y ** b) / c


def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "count"):
        fn_w_counter.count = 0

    fn_w_counter.count += 1

    caller_name = __name__
    return fn_w_counter.count, {caller_name: fn_w_counter.count}
