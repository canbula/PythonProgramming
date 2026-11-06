import inspect


# Calculate the power of a number
custom_power = lambda x=0, /, e=1: x ** e


# Calculate the result of a mathematical equation
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
    :param a: Coefficient of x.
    :param b: Coefficient of y.
    :param c: Divisor of the equation.
    :return: The calculated result as a float.
    """
    return (x * a + y * b) / c


# Count function calls and track caller information
def fn_w_counter():
    if not hasattr(fn_w_counter, "counter"):
        fn_w_counter.counter = 0
        fn_w_counter.callers = {}

    caller_frame = inspect.currentframe().f_back
    caller_name = caller_frame.f_globals.get("__name__", "__main__")

    fn_w_counter.counter += 1

    if caller_name in fn_w_counter.callers:
        fn_w_counter.callers[caller_name] += 1
    else:
        fn_w_counter.callers[caller_name] = 1

    return fn_w_counter.counter, fn_w_counter.callers.copy()