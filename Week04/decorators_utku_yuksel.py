def performance(func):
    def wrapper(*args, **kwargs):
        tm = __import__('tracemalloc')
        t = __import__('time')
        
        tm.start()
        start_time = t.perf_counter()
        
        result = func(*args, **kwargs)
        
        end_time = t.perf_counter()
        current, peak = tm.get_traced_memory()
        tm.stop()
        
        performance.counter += 1
        performance.total_time += (end_time - start_time)
        performance.total_mem += peak
        
        return result
    
    return wrapper

performance.counter = 0
performance.total_time = 0
performance.total_mem = 0
