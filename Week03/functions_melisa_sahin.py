custom_power = lambda x=0, /, e=1: x**e


def custom_equation(x=0, y=0, /, a=1, b=1, *, c=1) -> float:
    """
    This function adds the b power of the y variable to the a power of the x variable. Divides the result by variable c. 

    :param x: First base number, default is 0
    :param y: Second base number, default is 0
    :param a: First exponent number, default is 1
    :param b: Second exponent number, default is 1
    :param c: Division number, default is 1
    :return: Returns the result of the equation as a float
    :rtype: float

    """
    return (x**a + y**b) / c


def fn_w_counter():
    if not hasattr(fn_w_counter, "counter"):
        fn_w_counter.counter = 0
        fn_w_counter.caller_info = {}

    caller_name = __name__
    fn_w_counter.counter += 1

    if caller_name in fn_w_counter.caller_info:
        fn_w_counter.caller_info[caller_name] += 1
    else:
        fn_w_counter.caller_info[caller_name] = 1

    return (fn_w_counter.counter, fn_w_counter.caller_info)



