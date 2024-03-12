custom_power = lambda x = 0,/,e = 1: x**e

def custom_equation(x = 0,y = 0,/,a = 1,b = 1, * ,c = 1)->float:
    """
    This function
    :param x:The first number, default is 0
    :type x: int
    :param y:The second number, default is 0
    :type y: int
    :param a:The third number, default is 1
    :type a: int
    :param b:The fourth number, default is 1
    :type b: int
    :param c:The fifth number, default is 1
    :type c: int
    :return:The sum of 'x' power 'a' and 'y' power 'b' divided by c
    :rtype:float
    """   
    return (x**a + y**b) / c

def fn_w_counter() -> (int, dict[str,int]):
    if not hasattr(fn_w_counter, 'counter'):
        fn_w_counter.counter = 0
    
    fn_w_counter.counter += 1
    
    if not hasattr(fn_w_counter, 'callers'):
        fn_w_counter.callers = {f"{__name__}": 1}
    else:
        if __name__ in fn_w_counter.callers:
            fn_w_counter.callers[__name__] += 1
        else:
            fn_w_counter.callers[__name__] = 1

    
