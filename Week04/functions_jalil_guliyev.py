
custom_power = lambda x=0, /, e=1: x ** e


def custom_equation(
    x: int = 0, y: int = 0, /,
    a: int = 1, b: int = 1, *, c: int = 1
) -> float:
    """Calculate the result of an equation.

    :param x: First base.
    :param y: Second base.
    :param a: Exponent of x.
    :param b: Exponent of y.
    :param c: Divisor.
    :return: The result of (x**a + y**b) / c.
    """
    if any(type(value) is not int for value in (x, y, a, b, c)):
        raise TypeError("All parameters must be integers")

    return (x ** a + y ** b) / c


def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "counter"):
        fn_w_counter.counter = 0
        fn_w_counter.callers = {}

    fn_w_counter.counter += 1
    caller = __name__
    fn_w_counter.callers[caller] = (
        fn_w_counter.callers.get(caller, 0) + 1
    )

    return fn_w_counter.counter, fn_w_counter.callers.copy()
  
