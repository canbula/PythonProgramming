custom_power = lambda x = 0, /, e=1: x**e


def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    This function returns:
    The power of x to the a and
    the power of y to the b are
    added and divided by c.

    :param x : First Number
    :param y : Second Number
    :param a : Third Number
    :param b : Fourth Number
    :param c : Fifth Number
    :return: result as a floating-point number.
    """
    return float((x**a + y**b) / c)


def fn_w_counter():
    if not hasattr(fn_w_counter, "calls"):
        fn_w_counter.calls = 0
        fn_w_counter.caller_dict = {}
    caller_name = __name__
    fn_w_counter.calls += 1

    if caller_name in fn_w_counter.caller_dict:
        fn_w_counter.caller_dict[caller_name] += 1
    else:
        fn_w_counter.caller_dict[caller_name] = 1

    return fn_w_counter.calls, fn_w_counter.caller_dict
