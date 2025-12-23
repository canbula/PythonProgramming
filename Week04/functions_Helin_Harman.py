import inspect
import time
import tracemalloc
from functools import wraps


custom_power = lambda x, /, e=1: x**e  
result = custom_power(3)
print(f"Custom Power Sonucu: {result}")

def custom_equation(x=0, y=0, /, a=1, *, b=1, c=1) -> float:
    """
    This function calculates (x*a + y*b)/c
    """
    return (x*a + y*b)/c

result1 = custom_equation(3, 4, 5, b=4, c=2)
print(f"Custom Equation Sonucu: {result1}")


global_counter = 0
caller_log = {}

def fn_w_counter(c: int, d: dict) -> tuple[int, dict]:

    global global_counter
    
    caller_name = 'unknown_run' 
    try:
        caller_name = inspect.stack()[1].f_globals.get('__name__', 'system_call')
    except (IndexError, AttributeError, ValueError):
        caller_name = 'ide_console'
        
    global_counter += 1

    caller_log[caller_name] = caller_log.get(caller_name, 0) + 1
    
    return (global_counter, caller_log.copy())

def helper_test(val):
    return fn_w_counter(val, {})



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

@performance
def calculate_process_time(n):
    data = list(range(n))
    return sum(data)


if __name__ == '__main__':
    print("\n--- fn_w_counter Testi ---")
    fn_w_counter(1, {}) 
    count2, log2 = fn_w_counter(2, {})
    count3, log3 = helper_test(3)
    print(f"Toplam Çağrı: {count3}, Caller Log: {log3}")

    print("\n--- Performance Testi ---")
    calculate_process_time(500000)
    calculate_process_time(1000000)
    print(f"Toplam Çağrı Sayısı: {calculate_process_time.counter}")
    print(f"Toplam Süre: {calculate_process_time.total_time:.4f} sn")
    print(f"Toplam Bellek: {calculate_process_time.total_mem} byte")
