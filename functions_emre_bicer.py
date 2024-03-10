custom_power = lambda x=0,/,e=1 : x**e

def custom_equation(x:int=0, y:int=0, /, a:int=1, b:int=1, *, c:int=1) -> float:
    '''
    This function adds 2 exponents and divides by the value c
    
    Args:
        x(int): first exponential number's base
        y(int): second exponential number's base
        a(int): first exponential number's exponent
        b(int): second exponential number's exponent
        c(int): divisor value
    
    Returns:
        float: the result of sum of 2 exponents divided by c
    '''
    return (x**a + y**b) / c

def fn_w_counter():
    if not hasattr(fn_w_counter, "call_count"):
        fn_w_counter.call_count = 0
        fn_w_counter.caller_with_count = {}
    
    caller = __name__
    fn_w_counter.call_count += 1
    if caller in fn_w_counter.caller_with_count:
        fn_w_counter.caller_with_count[caller] += 1
    else:
        fn_w_counter.caller_with_count[caller] = 1

    return (fn_w_counter.call_count, fn_w_counter.caller_with_count)
