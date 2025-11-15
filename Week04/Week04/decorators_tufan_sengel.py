def performance(func):

    if not hasattr(performance, "call_count"):
        performance.call_count = 0

    if not hasattr(performance, "total_time"):
        performance.total_time = 0.0

    if not hasattr(performance, "total_memory"):
        performance.total_memory = 0.0
            

    def inner_function():
        import time
        import tracemalloc

        tracemalloc.start()
        start_time = time.perf_counter()
        start_memory = tracemalloc.get_traced_memory()[0]

        func()

        end_time = time.perf_counter()
        end_memory = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()

        elapsed_time = end_time - start_time
        memory_used = (end_memory - start_memory) / (1024**2)

        performance.call_count += 1
        performance.total_time += elapsed_time
        performance.total_memory += memory_used

        print(f"Function '{func.__name__}' call #{performance.call_count}:")
        print(f"Time taken: {elapsed_time:.6f} seconds")
        print(f"Memory used: {memory_used:.6f} MB")
        print(f"Total time for all calls: {performance.total_time:.6f} seconds")
        print(f"Total memory for all calls: {performance.total_memory:.6f} MB\n")

    return inner_function    

@performance
def sample_function():
    x = [i for i in range(1000000)] 
    return sum(x)

if __name__ == "__main__":
    sample_function()
    sample_function()
    sample_function()
