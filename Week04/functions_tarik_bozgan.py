custom_power = lambda x=0, /, e=1: x**e

def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculate a custom equation: (x**a + y**b) / c
    
    :param x: First base value (positional-only)
    :param y: Second base value (positional-only)
    :param a: Exponent for x (positional-or-keyword)
    :param b: Exponent for y (positional-or-keyword)
    :param c: Divisor (keyword-only)
    :return: The result of (x**a + y**b) / c
    :rtype: float
    """
    return (x**a + y**b) / c

def fn_w_counter() -> tuple[int, dict[str, int]]:
 
    caller = __name__

    if not hasattr(fn_w_counter, "total"):
        fn_w_counter.total = 0
    if not hasattr(fn_w_counter, "callers"):
        fn_w_counter.callers = {}

    fn_w_counter.total += 1
    fn_w_counter.callers[caller] = fn_w_counter.callers.get(caller, 0) + 1

    return fn_w_counter.total, fn_w_counter.callers.copy()



