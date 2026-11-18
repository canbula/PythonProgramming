import inspect



custom_power = lambda x=0, /, e=1: x ** e



def custom_equation(
    x: int = 0,
    y: int = 0,
    /,
    a: int = 1,
    b: int = 1,
    *,
    c: int = 1,
) -> float:
    """
    Calculates the value of (x**a + y**b) / c.

    :param x: Base of the first term (positional-only)
    :param y: Base of the second term (positional-only)
    :param a: Exponent of x (positional-or-keyword)
    :param b: Exponent of y (positional-or-keyword)
    :param c: Divisor (keyword-only)
    :return: Result of (x**a + y**b) / c as a float
    """
    return (x ** a + y ** b) / c



def fn_w_counter() -> tuple[int, dict[str, int]]:
    if not hasattr(fn_w_counter, "total_calls"):
        fn_w_counter.total_calls = 0
        fn_w_counter.callers = {}

    caller_name = inspect.currentframe().f_back.f_globals.get("__name__", "__main__")

    fn_w_counter.total_calls += 1
    fn_w_counter.callers[caller_name] = fn_w_counter.callers.get(caller_name, 0) + 1

    return fn_w_counter.total_calls, fn_w_counter.callers
