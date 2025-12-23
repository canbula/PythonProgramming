import inspect

custom_power = lambda x=0, /, e=1: x**e

def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Computes the result of the equation (x**a + y**b) / c.

    :param x: The first base integer
    :type x: int
    :param y: The second base integer
    :type y: int
    :param a: The first exponent
    :type a: int
    :param b: The second exponent
    :type b: int
    :param c: The divisor
    :type c: int
    :return: The result of the equation as a float
    :rtype: float
    """
    return (x**a + y**b) / c

def fn_w_counter() -> tuple[int, dict]:
    if not hasattr(fn_w_counter, 'total_calls'):
        fn_w_counter.total_calls = 0
        fn_w_counter.caller_counts = {}
    
    fn_w_counter.total_calls += 1
    
    try:
        frame = inspect.currentframe().f_back
        caller_name = frame.f_globals['__name__']
    except (AttributeError, KeyError):
        caller_name = 'unknown'

    if caller_name in fn_w_counter.caller_counts:
        fn_w_counter.caller_counts[caller_name] += 1
    else:
        fn_w_counter.caller_counts[caller_name] = 1
        
    return fn_w_counter.total_calls, fn_w_counter.caller_counts
