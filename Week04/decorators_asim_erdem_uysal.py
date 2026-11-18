import tracemalloc
import time


def performance(fn):
    def wrapper(*args, **kwargs):

        performance.counter +=1

        tracemalloc.start() 
        baslangic = time.time()

        sonuc = fn(*args, **kwargs)  

        bitis = time.time()
        current ,peak = tracemalloc.get_traced_memory()  

        tracemalloc.stop()  

       
        performance.total_time += bitis-baslangic
        performance.total_mem +=peak

        return sonuc 
                        
    return wrapper



performance.counter = 0     
performance.total_time = 0
performance.total_mem = 0


