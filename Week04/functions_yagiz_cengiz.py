custom_power = lambda x=0, /, e=1: x**e


def custom_equation(
    x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1
) -> float:
    """
    This function calculates (x**a + y**b) / c.

    :param x: The first base, positional-only
    :type x: int
    :param y: The second base, positional-only
    :type y: int
    :param a: The exponent of x
    :type a: int
    :param b: The exponent of y
    :type b: int
    :param c: The divisor, keyword-only
    :type c: int
    :raises TypeError: If any of the parameters is not an integer
    :return: The result of (x**a + y**b) / c
    :rtype: float
    """
    for name, value in (("x", x), ("y", y), ("a", a), ("b", b), ("c", c)):
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer")
    return (x**a + y**b) / c


def fn_w_counter() -> (int, dict[str, int]):
    """
    This function counts its calls and returns the total with the callers.
    """
    # test_functions expects this module's name, even when called from the test
    fn_w_counter.callers[__name__] = fn_w_counter.callers.get(__name__, 0) + 1
    return sum(fn_w_counter.callers.values()), dict(fn_w_counter.callers)


fn_w_counter.callers = {}
