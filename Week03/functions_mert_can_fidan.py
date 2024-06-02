custom_power = lambda x = 0, /, e = 1: x**e 
    
    
def custom_equation(x: int = 0,
                    y: int = 0,
                    /,
                    a: int = 1,
                    b: int = 1,
                    *,
                    c: int = 1) -> float:
    """
    This fuction firstly calculates
    the a power of the number x and
    the b power of the number y after that
    adds up calculated numbers and
    divedes the result by c.
    
    :param x: The first number, positional-only and default value 0
    :type x: int
    :param y: The second number, positional-only and default value 0
    :type y: int
    :param a: The third number, positional-or-keyword and default value 1
    :type a: int
    :param b: The fourth number, positional-or-keyword and default value 1
    :type b: int
    :param c: The fifth number, positional-or-keyword and default value 1
    :type c: int
    :return: result of equation
    :rtype: float
    """
    return (x**a + y**b)/c


def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "total_calls"):
        fn_w_counter.total_calls = 0
        fn_w_counter.callers_information = {}
    
    caller_name = __name__
    fn_w_counter.total_calls += 1
    
    if caller_name in fn_w_counter.callers_information:
        fn_w_counter.callers_information[caller_name] += 1
    else:
        fn_w_counter.callers_information[caller_name] = 1    

    return fn_w_counter.total_calls, fn_w_counter.callers_information
