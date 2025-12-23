import inspect
import time
import tracemalloc
from functools import wraps

custom_power = lambda x=0, /, e=1: x**e  


def custom_equation(x=0, y=0, /, a=1, *, b=1, c=1) -> float:
    """
    This function calculates (x*a + y*b)/c
    :param x: first value
    :param y: second value
    :param a: multiplier for x
    :param b: multiplier for y
    :param c: divisor
    """
    return (x*a + y*b)/c

global_counter = 0
caller_log = {}

def fn_w_counter(c: int, d: dict) -> tuple[int, dict[str, int]]:
    global global_counter
    # Flake8 F824 hatasını önlemek için 'global caller_log' kaldırıldı.
    
    caller_name = 'unknown_run' 
    try:
        caller_name = inspect.stack()[1].f_globals.get('__name__', 'system_call')
    except (IndexError, AttributeError, ValueError):
        caller_name = 'ide_console'
        
    global_counter += 1
    caller_log[caller_name] = caller_log.get(caller_name, 0) + 1
    
    return (global_counter, caller_log.copy())

def performance(func):
    @wraps(func)
    def _performance(*args, **kwargs):
        tracemalloc.start()
        t1 = time.perf_counter()
        
        result = func(*args, **kwargs)
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        t2 = time.perf_counter()
        
        _performance.counter += 1
        _performance.total_time += (t2 - t1)
        _performance.total_mem += peak
        
        return result
    
    _performance.counter = 0
    _performance.total_time = 0.0
    _performance.total_mem = 0
    return _performance
