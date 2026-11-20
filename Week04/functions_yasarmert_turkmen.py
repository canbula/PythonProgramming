custom_power = lambda x=0, / , e=1: x**e

def custom_equation(x:int=0,y:int=0,/,a:int=1,b:int=1,*,c:int=1) -> float:
    """
    Calculates a custom equation

    :param x: Base value for the first term. The default value is 0
    :param y: Base value for the second term. The default value is 0
    :param a: Exponent for the first term. The defaults value is 1.
    :param b: Exponent for the second term. The defaults value is 1.
    :param c: The divisor. The default value is 1
    :return: Returns the float number that is the result of the calculated custom equation.
    """
    return (x**a + y**b) / c

def fn_w_counter() -> (int, dict[str,int]):
    if not hasattr(fn_w_counter, "total_calls"):
        fn_w_counter.total_calls = 0
        fn_w_counter.caller_dict = {}

    caller = __name__

    fn_w_counter.total_calls += 1
    fn_w_counter.caller_dict[caller] = fn_w_counter.caller_dict.get(caller, 0) + 1

    return fn_w_counter.total_calls, fn_w_counter.caller_dict
