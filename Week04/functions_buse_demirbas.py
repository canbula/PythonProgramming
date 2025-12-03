def custom_power(x , / , e=1)
    return x**e
def custom_equation(x=0 , y=0, / , a=1 , b=1, * , c=1) -> float:
    return (x**a + y**b)/c
def fn_w_counter():
    if not hasattr(fn_w_counter, "total_calls"):
        fn_w_counter.total_calls = 0
    if not hasattr(fn_w_counter, "callers"):
        fn_w_counter.callers = {}
