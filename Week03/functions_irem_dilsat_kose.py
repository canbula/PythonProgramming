custom_power = lambda x, /, e=1 : x**e

def custom_equation(x: int, y: int, /, a: int = 1, b: int = 1, *, c: int = 1)-> float:
    """
    This function computes the expression (x**a + y**b)/c

    :param x:The first number, default=0
    :type x:int
    :param y:The second number, default=0
    :type y:int
    :param a:The third number, default=1
    :type a:int
    :param b:The fourth number, default=1
    :type b:int
    :param c:The fifth number, default=1
    :type c:int
    :return: The result of the equation (x**a + y**b)/c
    :rtype: float

    """
    return (x**a + y**b) / c

def fn_w_counter() -> (int, dict[str,int]):
    if not hasattr(fn_w_counter,"call_counter"):
        fn_w_counter.call_counter = 0
        fn_w_counter.caller_counts = {}
    
    caller_name = __name__
    fn_w_counter.call_counter +=1
    
    if caller_name in fn_w_counter.caller_counts:
        fn_w_counter.caller_counts[caller_name] +=1
        
    else:
        fn_w_counter.caller_counts[caller_name] =1

    return fn_w_counter.call_counter, fn_w_counter.caller_counts
