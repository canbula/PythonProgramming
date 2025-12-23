import time
import functools
import tracemalloc

def performance(func):
    """
    Fonksiyon performansını ölçen ve istatistikleri (sayaç, süre, bellek) 
    kendi özniteliklerinde saklayan bir dekoratör.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        wrapper.counter += 1
        

        tracemalloc.start()
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:

            end_time = time.perf_counter()
            duration = end_time - start_time
            wrapper.total_time += duration
            

            _, peak = tracemalloc.get_traced_memory()
            wrapper.total_mem += peak
            tracemalloc.stop()
          
    wrapper.counter = 0
    wrapper.total_time = 0.0
    wrapper.total_mem = 0
    
    return wrapper

@performance
def test_function(n):

    return [i**2 for i in range(n)]

if __name__ == "__main__":
    test_function(100000)
    test_function(200000)

    print(f"Fonksiyon {test_function.counter} kez çağrıldı.")
    print(f"Toplam süre: {test_function.total_time:.4f} saniye")
    print(f"Toplam bellek tüketimi: {test_function.total_mem} byte")
