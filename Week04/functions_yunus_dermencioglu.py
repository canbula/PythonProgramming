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
    Calculate the result of a mathematical equation.

    :param x: First integer value.
    :param y: Second integer value.
    :param a: Exponent of x.
    :param b: Exponent of y.
    :param c: Divisor of the equation.
    :return: The calculated result as a float.
    """
    return (x ** a + y ** b) / c


def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "counter"):
        fn_w_counter.counter = 0
        fn_w_counter.callers = {}

    caller_name = inspect.currentframe().f_back.f_code.co_name

    if caller_name == "<module>":
        caller_name = "__main__"

    fn_w_counter.counter += 1

    if caller_name in fn_w_counter.callers:
        fn_w_counter.callers[caller_name] += 1
    else:
        fn_w_counter.callers[caller_name] = 1

    return fn_w_counter.counter, fn_w_counter.callers.copy()
