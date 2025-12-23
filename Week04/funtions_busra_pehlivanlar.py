import sys

custom_power = lambda x=0, /, e=1: x**e

def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    return float((x**a + y**b) / c)

def fn_w_counter():
    if not hasattr(fn_w_counter, "calls"):
        fn_w_counter.calls = 0
        fn_w_counter.callers = {}
    
    try:
        caller_name = sys._getframe(1).f_globals.get('__name__', '__main__')
    except:
        caller_name = "__main__"
        
    fn_w_counter.calls += 1
    fn_w_counter.callers[caller_name] = fn_w_counter.callers.get(caller_name, 0) + 1
    
    return (fn_w_counter.calls, fn_w_counter.callers)
