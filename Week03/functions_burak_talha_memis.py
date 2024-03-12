custom_power = lambda x = 0,/,e = 1: x**e

def custom_equation(x = 0,y = 0,/,a = 1,b = 1, * ,c = 1)->float:
    return (x**a + y**b) / c
'''
x is positional-only with default value 0
y is positional-only with default value 0
a is positional-or-keyword with default value 1
b is positional-or-keyword with default value 1
c is keyword-only with default value 1
'''    

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
    
