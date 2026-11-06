custom_power = lambda x=0, /, e=1: x ** e

def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Calculates the result of a custom mathematical equation.

    :param x: The first base (positional-only).
    :param y: The second base (positional-only).
    :param a: The exponent for the first base (positional-or-keyword).
    :param b: The exponent for the second base (positional-or-keyword).
    :param c: The divisor (keyword-only).
    :return: The result of the equation (x**a + y**b) / c as a float.
    """
    if type(x) is not int or type(y) is not int or type(a) is not int or type(b) is not int or type(c) is not int:
        raise TypeError("All arguments must be integers.")
        
    return float((x ** a + y ** b) / c)

def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "total_calls"):
        fn_w_counter.total_calls = 0
        fn_w_counter.caller_dict = {}
        
    fn_w_counter.total_calls += 1
    
    caller = __name__ 
    
    if caller not in fn_w_counter.caller_dict:
        fn_w_counter.caller_dict[caller] = 0
    fn_w_counter.caller_dict[caller] += 1
    
    return fn_w_counter.total_calls, fn_w_counter.caller_dict
