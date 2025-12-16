custom_power = lambda x=0, /, e=1: x**e

def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates the result based on the provided formula.

    :param x: The positional-only integer base parameter, default is 0
    :param y: The positional-only integer base parameter, default is 0
    :param a: The positional-or-keyword integer exponent parameter, default is 1
    :param b: The positional-or-keyword integer exponent parameter, default is 1
    :param c: The keyword-only integer divisor parameter, default is 1
    :return: The result of (x**a + y**b)/c as a float
    :rtype: float
    """
    return float((x**a + y**b) / c)

def fn_w_counter() -> tuple:
    if not hasattr(fn_w_counter, 'call_counter'):
        fn_w_counter.call_counter = 0
        fn_w_counter.caller_stats = {}
    
    caller_name = __name__

    fn_w_counter.call_counter += 1

    if caller_name in fn_w_counter.caller_stats:
        fn_w_counter.caller_stats[caller_name] += 1
    else:
        fn_w_counter.caller_stats[caller_name] = 1

    return fn_w_counter.call_counter, fn_w_counter.caller_stats
