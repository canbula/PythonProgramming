custom_power = lambda x=0, /, e=1: x**e

def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates a custom equation.

    :param x: Positional-only integer, defaults to 0.
    :param y: Positional-only integer, defaults to 0.
    :param a: Positional-or-keyword integer, defaults to 1.
    :param b: Positional-or-keyword integer, defaults to 1.
    :param c: Keyword-only integer, defaults to 1.
    :return: The result of (x**a + y**b) / c as float.
    """
    if not all(isinstance(val, int) for val in (x, y, a, b, c)):
        raise TypeError("Arguments must be integers.")
        
    return float((x**a + y**b) / c)

def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "total_calls"):
        fn_w_counter.total_calls = 0
        fn_w_counter.caller_counts = {}
    
    caller_name = __name__

    fn_w_counter.total_calls += 1
    
    if caller_name in fn_w_counter.caller_counts:
        fn_w_counter.caller_counts[caller_name] += 1
    else:
        fn_w_counter.caller_counts[caller_name] = 1

    return (fn_w_counter.total_calls, fn_w_counter.caller_counts)