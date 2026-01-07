import inspect

# 1. custom_power: lambda function with positional-only x
custom_power = lambda x=0, /, e=1: x**e

# 2. custom_equation: positional-only, positional-or-keyword, and keyword-only params
def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates (x**a + y**b) / c with specific parameter constraints.

    :param x: Base 1, positional-only
    :param y: Base 2, positional-only
    :param a: Exponent 1, positional-or-keyword
    :param b: Exponent 2, positional-or-keyword
    :param c: Divisor, keyword-only
    :returns: Result as float
    """
    return float((x**a + y**b) / c)

# 3. fn_w_counter: tracks total calls and caller names
def fn_w_counter() -> tuple[int, dict]:
    """
    Counts the number of calls and tracks the caller (__name__).
    """
    if not hasattr(fn_w_counter, "calls"):
        fn_w_counter.calls = 0
        fn_w_counter.callers = {}

    caller_frame = inspect.currentframe().f_back
    caller_name = caller_frame.f_globals.get('__name__', 'unknown')

    fn_w_counter.calls += 1
    fn_w_counter.callers[caller_name] = fn_w_counter.callers.get(caller_name, 0) + 1

    return (fn_w_counter.calls, fn_w_counter.callers)
