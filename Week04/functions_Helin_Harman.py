custom_power = lambda x, /, e=1: x**e  

result = custom_power(3)
print(result)

def custom_equation(x=0, y=0, /, a=1, *, b=1, c=1) -> float:
    """
    This function calculates
    (x*a + y*b)/c
    """
    return (x*a + y*b)/c

result1 = custom_equation(3, 4, 5, b=4, c=2)
print(result1)


import inspect

global_counter = 0
caller_log = {}

def fn_w_counter (c: int, d: dict) -> tuple[int, dict]:
    global global_counter
    global caller_log
    
    caller_name = 'unknown_run' 
    try:
        # inspect.stack()[1] normalde '__main__' veya 'fonksiyon_adı'nı bulur.
        caller_name = inspect.stack()[1].f_globals.get('__name__', 'system_call')
    except (IndexError, AttributeError, ValueError):
        caller_name = 'ide_console' # Hata durumunda bunu logla
        
    global_counter += 1
    caller_log[caller_name] = caller_log.get(caller_name, 0) + 1
    
    return (global_counter, caller_log.copy())

def helper_test(val):
    return fn_w_counter(val, {})

if __name__ == '__main__':
    print("--- fn_w_counter Gelişmiş Testi ---")
    

    fn_w_counter(1, {}) 

    count2, log2 = fn_w_counter(2, {})
    print(f"1. Aşamadan Toplam: {count2}, Log: {log2}")


    count3, log3 = helper_test(3)
    print(f"2. Aşamadan Toplam: {count3}, Log: {log3}")
    

import time
import tracemalloc
from functools import wraps

def performance(func):
    @wraps(func) #docstringi korur
    def _performance(*args, **kwargs):
        

        tracemalloc.start()
        t1 = time.perf_counter()

        result = func(*args, **kwargs)

        current, peak = tracemalloc.get_traced_memory() #bellek kullanımı
        tracemalloc.stop()
        t2 = time.perf_counter()
        
        elapsed_time = t2 - t1
        

        _performance.counter += 1
        _performance.total_time += elapsed_time
        _performance.total_mem += peak
        
        return result
    
    _performance.counter = 0
    _performance.total_time = 0.0
    _performance.total_mem = 0

    return _performance

@performance
def calculate_process_time(n):
    data = list(range(n))
    result = sum(data)
    return result

print("Performance dekoratif testi")

resulta =calculate_process_time(500000)
print(resulta)

calculate_process_time(1000000)

print(" ")

print("sonuçlar : ")

print(f"Toplam Çağrı Sayısı (counter): {calculate_process_time.counter}")
print(f"Toplam Süre (total_time): {calculate_process_time.total_time:.4f} saniye")
print(f"Toplam Bellek (total_mem): {calculate_process_time.total_mem} byte")
