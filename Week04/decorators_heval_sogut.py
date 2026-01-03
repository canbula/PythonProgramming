import time
import tracemalloc

def performance(func):
  
    # This is the wrapper function.
    def wrapper(*args, **kwargs):
        """Wrapper function that adds performance tracking."""
        
        # --- "Before" logic ---
        tracemalloc.start()
        start_time = time.perf_counter()

        # Execute the original function
        result = func(*args, **kwargs)

        # --- "After" logic ---
        # Get performance metrics
        end_time = time.perf_counter()
        _current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        elapsed_time = end_time - start_time

        # Update the statistics
        performance.counter += 1
        performance.total_time += elapsed_time
        performance.total_mem += peak_mem

        return result
    
    # The decorator returns the new wrapper function
    return wrapper

# Initialize the state as attributes of the function object.
# This state will be shared across all uses of the @performance decorator.
performance.counter = 0
performance.total_time = 0.0
performance.total_mem = 0
