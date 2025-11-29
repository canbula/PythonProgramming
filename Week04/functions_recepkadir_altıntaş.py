custom_power = lambda x=0, /, e=1: x ** e

def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates the result.

    :param x: Base number 1
    :param y: Base number 2
    :param a: Exponent for x
    :param b: Exponent for y
    :param c: Divisor
    :return: The calculated result as a float
    """
    if not all(isinstance(arg, int) for arg in [x, y, a, b, c]):
        raise TypeError("All arguments must be integers.")
    return float((x ** a + y ** b) / c)

def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "count"):
        fn_w_counter.count = 0
    fn_w_counter.count += 1
    return fn_w_counter.count, {__name__: fn_w_counter.count}
