import time
import sys
def performance(func):
    if not hasattr(performance,"counter"):
        setattr(performance,"counter",0)
    
    if not hasattr(performance,"total_time"):
        setattr(performance,"total_time",0)
    
    if not hasattr(performance,"total_mem"):
        setattr(performance,"total_mem",0)
    
    def _d1():
         memory_used = sys.getsizeof(func)
         start_time = time.time_ns()
         func()
         performance.counter += 1
         end_time = time.time_ns()
         elapsed = 0
         elapsed = end_time - start_time
         performance.total_time += (int)(elapsed/1e9)
         performance.total_mem += memory_used
         return (performance.counter, performance.total_time, performance.total_mem)

    return _d1
    

if __name__ == "__main__":
    @performance
    def function_to_test():
        time.sleep(1)

    def function():
        for i in range(1):
            function_to_test()
    function()
    print(function_to_test())
