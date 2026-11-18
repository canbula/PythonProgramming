import inspect
from typing import Tuple, Dict

custom_power = lambda x=0, /, e=1: x**e

def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Computes the custom equation (x**a + y**b) / c.

    :param x: First positional-only base integer.
    :param y: Second positional-only base integer.
    :param a: First positional-or-keyword exponent integer.
    :param b: Second positional-or-keyword exponent integer.
    :param c: Keyword-only divisor integer.
    :return: The result of the equation as a float.
    """
    return float((x**a + y**b) / c)

def fn_w_counter() -> Tuple[int, Dict[str, int]]:
    if not hasattr(fn_w_counter, "caller_counts"):
        fn_w_counter.caller_counts = {}
        fn_w_counter.total_calls = 0

    frame = inspect.currentframe().f_back
    caller_name = frame.f_globals.get('__name__', 'unknown')

    fn_w_counter.total_calls += 1
    fn_w_counter.caller_counts[caller_name] = fn_w_counter.caller_counts.get(caller_name, 0) + 1

    return (fn_w_counter.total_calls, fn_w_counter.caller_counts)
