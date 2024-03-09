custom_power = lambda x=0,/  , e=1 : x**e

def custom_equation(x:int = 0, y:int = 0, /, a:int = 1, b:int = 1, *, c:int = 1) -> float:
    """
    This funciton  calculates the value of an equation given certain parameters
    :param x: The first number, default is 0
    :type x: int
    :param y: The second number, default is  0
    :type y: int
    :param a: The coefficient for x in the equation, default is 1
    :type a: int
    :param b: The coefficient for y in the equation, default is 1
    :type b: int
    :param c:  A constant term in the equation, default is 
    :type c: int
    :return : The result of the equation with the given values
    :rtype: int
    """
    return (x**a + y**b)/c

def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter, "call_count"):
        fn_w_counter.call_count = 0
        fn_w_counter._dict = {}
    caller_name = __name__
    fn_w_counter.call_count += 1
    if caller_name in fn_w_counter._dict:
        fn_w_counter._dict[caller_name] += 1
    else:
        fn_w_counter._dict[caller_name] = 1
    return fn_w_counter.call_count, fn_w_counter._dict
