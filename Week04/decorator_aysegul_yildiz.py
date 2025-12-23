import time
import tracemalloc

def performans(func):
    """Bir fonksiyonun zaman ve bellek tüketimini ölçen dekoratör."""

    def sarmalayıcı(*args, **kwargs):
        # --- ÖNCE ---
        tracemalloc.start()
        baslangic = time.perf_counter()

        # Fonksiyonun gerçek çalışması
        sonuc = func(*args, **kwargs)

        # --- SONRA ---
        bitis = time.perf_counter()
        mevcut_bellek, maksimum_bellek = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        gecen_sure = bitis - baslangic

        # Performans istatistiklerini güncelle
        performans.sayac += 1
        performans.toplam_sure += gecen_sure
        performans.toplam_bellek += maksimum_bellek

        # Ölçüm sonuçlarını kullanıcıya göster
        print(f"Fonksiyon adı: {func.__name__}")
        print(f"Geçen süre: {gecen_sure:.10f} saniye")
        print(f"Bellek kullanımı: {maksimum_bellek} bayt")
        print(f"Toplam çağrı sayısı: {performans.sayac}\n")

        return sonuc

    return sarmalayıcı

# Dekoratörün durum değişkenlerini başlat 
performans.sayac = 0
performans.toplam_sure = 0.0
performans.toplam_bellek = 0
