import time
import tracemalloc

def performance(f):
    if not hasattr(performance, "counter"):
        performance.counter = 0
    if not hasattr(performance, "total_time"):
        performance.total_time = 0.0
    if not hasattr(performance, "total_mem"):
        performance.total_mem = 0
        
    def _performance(*args, **kwargs):
        # Çağırılma sayısı
        performance.counter += 1 
        
        # Takip başlat
        tracemalloc.start()
        x = time.time()
        
        # Fonksiyonu çağır
        ret = f(*args, **kwargs)

        # süreyi kaydet
        performance.total_time += time.time() - x
        # bellek tüketimini kaydet
        performance.total_mem = tracemalloc.get_traced_memory()[1]
        # takibi bırak
        tracemalloc.stop()

        return ret
    return _performance