custom_power = lambda x=0, /, e=1: x**e

def custom_equation(x: int = 0 , y: int = 0 , / , a: int =1 , b: int =1, * , c: int=1) -> float:
    """
    Calculates the custom equation.
    :param x: first base
    :type x: int
    :param y: second base
    :type y: int
    :param a: exponent for x
    :type a: int
    :param b: exponent for y
    :type b: int
    :param c: divisor
    :type c: int
    :return: the result of (x**a + y**b) / c
    :rtype: float 
    """

    return float((x**a + y**b) / c)


def fn_w_counter() -> (int, dict[str,int]):
    if not hasattr(fn_w_counter,"total_count"):
        fn_w_counter.total_count = 0
        fn_w_counter.call_records = {}

    caller = __name__
    fn_w_counter.total_count += 1

    if caller not in fn_w_counter.call_records:
        fn_w_counter.call_records[caller] = 1
    else:
        fn_w_counter.call_records[caller] += 1

    return fn_w_counter.total_count, fn_w_counter.call_records


    
