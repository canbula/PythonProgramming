custom_power = lambda x=0,/,e=1 : x**e

def custom_equation(x: int =0, y:int=0,/, a: int=1, b:int =1,*,c:int = 1) ->float:
    '''
    This function returns x to the power of a plus y to the power of b divided by c,
    :param x : is the first number
    :param y : is the second number
    :param a : is the third number
    :param b : is the fourth number
    :param c : is the fifth number 
    :return : As a floating-point number.
    
    '''
    return float((x**a + y**b)/c)

def fn_w_counter() -> (int, dict[str,int]):
    if not hasattr(fn_w_counter,"call_counter"):
        fn_w_counter.call_counter = 0
        fn_w_counter.caller_counts = {}
    
    caller_name = __name__
    fn_w_counter.call_counter +=1
    
    if caller_name in fn_w_counter.caller_counts:
        fn_w_counter.caller_counts[caller_name] +=1
    else:
        fn_w_counter.caller_counts[caller_name] =1

    return fn_w_counter.call_counter, fn_w_counter.caller_counts
