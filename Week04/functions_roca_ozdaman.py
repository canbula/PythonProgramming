custom_power = lambda x=0, /, e=1: x ** e

def custom_equation(x: int = 0, y: int = 0,/, a: int = 1, b: int = 1,*, c: int = 1) -> float:
    """
    Calculates a custom equation.

    :param x: Positional-only integer.
    :param y: Positional-only integer.
    :param a: Exponent for x.
    :param b: Exponent for y.
    :param c: Divisor.
    :return: Result of (x**a + y**b) / c
    """
    return (x ** a + y ** b) / c

def fn_w_counter() -> (int, dict[str, int]):
    if not hasattr(fn_w_counter,'_call_counter'):
        fn_w_counter._call_counter = 0
        fn_w_counter._caller_dict = {}
    caller = __name__
    fn_w_counter._call_counter += 1
    if caller in fn_w_counter._caller_dict:
        fn_w_counter._caller_dict[caller] += 1
    else:
        fn_w_counter._caller_dict[caller] = 1
    return fn_w_counter._call_counter,fn_w_counter._caller_dict
