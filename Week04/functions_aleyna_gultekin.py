custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Raises x to the power a and y to the power b, adds them and divides by c.

    :param x: Base of the first term (positional-only)
    :type x: int
    :param y: Base of the second term (positional-only)
    :type y: int
    :param a: Power applied to x
    :type a: int
    :param b: Power applied to y
    :type b: int
    :param c: Number to divide the sum by (keyword-only)
    :type c: int
    :return: The calculated value
    :rtype: float
    """
    for name, value in (("x", x), ("y", y), ("a", a), ("b", b), ("c", c)):
        if type(value) is not int:
            raise TypeError(f"{name} must be an int")
    return float((x ** a + y ** b) / c)


def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "call_count"):
        fn_w_counter.call_count = 0
        fn_w_counter.callers = {}

    fn_w_counter.call_count += 1
    if __name__ in fn_w_counter.callers:
        fn_w_counter.callers[__name__] += 1
    else:
        fn_w_counter.callers[__name__] = 1

    return fn_w_counter.call_count, fn_w_counter.callers
