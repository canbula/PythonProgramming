custom_power = lambda x=0,/,e=1: x ** e

def custom_equation(x: int = 0 , y: int = 0, / , a: int = 1, b: int = 1, * , c: int = 1) -> float:
    """
    Calculate the custom equation (x**a + y**b) / c.

    :param x: first base
    :param y: second base
    :param a: first exponent
    :param b: second exponent
    :param c: divisor
    :return: the computed float result
    """
    return (x**a + y**b) / c


def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter,'call_counter'):
        fn_w_counter.call_counter = 0
        fn_w_counter.caller_dict = {}
    caller = __name__
    fn_w_counter.call_counter += 1
    if caller in fn_w_counter.caller_dict:
        fn_w_counter.caller_dict[caller] += 1
    else:
        fn_w_counter.caller_dict[caller] = 1
    return fn_w_counter.call_counter,fn_w_counter.caller_dict
