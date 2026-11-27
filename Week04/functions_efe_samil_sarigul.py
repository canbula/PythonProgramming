custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    This function calculates (x**a + y**b) / c.

    :param x: First base, positional-only
    :param y: Second base, positional-only
    :param a: Exponent of x
    :param b: Exponent of y
    :param c: Divisor, keyword-only
    :return: The result of (x**a + y**b) / c
    """
    for value in (x, y, a, b, c):
        if type(value) is not int:
            raise TypeError("All parameters must be integers.")
    return (x ** a + y ** b) / c


def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "call_counter"):
        fn_w_counter.call_counter = 0
        fn_w_counter.callers = {}
    fn_w_counter.call_counter += 1
    if __name__ in fn_w_counter.callers:
        fn_w_counter.callers[__name__] += 1
    else:
        fn_w_counter.callers[__name__] = 1
    return fn_w_counter.call_counter, fn_w_counter.callers
