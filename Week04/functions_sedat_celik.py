custom_power = lambda x=0, /, e=1: x**e

def custom_equation(x: int = 0 , y: int = 0 , / , a: int =1 , b: int =1, * , c: int=1) -> float:
    """
    Calculates and returns the custom equation
    
    :param x: first positional-only base value, default is 0
    :type x: int
    :param y: second positional-only value, default is 0
    :type y: int
    :param a: exponent of x, default is 1
    :type a: int
    :param b: exponent of y, default is 1
    :type b: int
    :param c: keyword-only divisor value, default is 1
    :type c: int
    :return: the calculated result of the equation (x**a + y**b) / c
    :rtype: float 
    """

    return float((x**a + y**b) / c)


def fn_w_counter() -> tuple[int, dict[str, int]]:
    if not hasattr(fn_w_counter, "total_calls"):
        fn_w_counter.total_calls = 0
        fn_w_counter.caller_counts = {}

    caller = __name__

    fn_w_counter.total_calls += 1
    fn_w_counter.caller_counts[caller] = (
        fn_w_counter.caller_counts.get(caller, 0) + 1
    )

    return fn_w_counter.total_calls, dict(fn_w_counter.caller_counts)
