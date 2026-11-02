custom_power = lambda a=0,/,e=1: a ** e

def custom_equation(a: int = 0 , b: int = 0, / , x: int = 1, y: int = 1, * , z: int = 1) -> float:
    """
    Calculate the custom equation (a**x + b**y) / z.

    :param a: first base
    :param b: second base
    :param x: first exponent
    :param y: second exponent
    :param z: divisor
    :return: the computed float result
    """
    return (a**x + b**y) / z


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
