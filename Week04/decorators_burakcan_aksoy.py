import time
import sys
import functools


class performance:
    """
    A decorator which measures the performance of functions and saves statistics.
    
    Attributes:
        counter: Number of times the decorator has been called
        total_time: Total time in seconds that decorated functions took
        total_mem: Total memory in bytes that decorated functions consumed
    """
    counter = 0
    total_time = 0
    total_mem = 0
    
    def __init__(self, func):
        """Initialize the decorator with the function to be decorated."""
        self.func = func
        functools.update_wrapper(self, func)
    
    def __call__(self, *args, **kwargs):
        """
        Execute the decorated function and track performance metrics.
        
        :param args: Positional arguments for the function
        :param kwargs: Keyword arguments for the function
        :return: The result of the decorated function
        """
        # Increment counter
        performance.counter += 1
        
        # Measure time
        start_time = time.time()
        
        # Get memory before execution
        mem_before = sys.getsizeof(args) + sys.getsizeof(kwargs)
        
        # Execute the function
        result = self.func(*args, **kwargs)
        
        # Measure time taken
        end_time = time.time()
        elapsed_time = end_time - start_time
        performance.total_time += elapsed_time
        
        # Get memory after execution (including result)
        mem_after = sys.getsizeof(result) if result is not None else 0
        performance.total_mem += mem_after
        
        return result
