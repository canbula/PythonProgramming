import inspect
from typing import Tuple, Dict

# 1. custom_power
# x sadece pozisyonel (positional-only) olduğu için '/' öncesinde yer alır.
# e pozisyonel veya anahtar kelime olabileceği için '/' sonrasındadır.
custom_power = lambda x=0, /, e=1: x**e


# 2. custom_equation
# x ve y sadece pozisyonel (/), a ve b her ikisi de olabilir, c sadece anahtar kelime (*)
def custom_equation(x: int = 0, y: int = 0, /, a: int = 1, b: int = 1, *, c: int = 1) -> float:
    """
    Belirtilen formülü hesaplar: (x**a + y**b) / c

    :param x: İlk taban değeri, varsayılan 0.
    :type x: int
    :param y: İkinci taban değeri, varsayılan 0.
    :type y: int
    :param a: x için üs, varsayılan 1.
    :type a: int
    :param b: y için üs, varsayılan 1.
    :type b: int
    :param c: Bölen, varsayılan 1.
    :type c: int
    :return: Hesaplamanın sonucu.
    :rtype: float
    """
    return float((x**a + y**b) / c)


# 3. fn_w_counter
# Fonksiyonun çağrılma sayısını ve çağıran modülün bilgisini tutar.
def fn_w_counter() -> Tuple[int, Dict[str, int]]:
    # Fonksiyonun kendi üzerinde değişkenler (state) oluşturarak sayaçları tutuyoruz.
    if not hasattr(fn_w_counter, 'total_calls'):
        fn_w_counter.total_calls = 0
        fn_w_counter.caller_info = {}

    # Toplam çağrı sayısını artır
    fn_w_counter.total_calls += 1

    # Çağıranın (caller) __name__ bilgisini al (örn: '__main__')
    frame = inspect.currentframe().f_back
    caller_name = frame.f_globals.get('__name__', 'unknown')

    # Çağıran modülün sayacını güncelle
    fn_w_counter.caller_info[caller_name] = fn_w_counter.caller_info.get(caller_name, 0) + 1

    return fn_w_counter.total_calls, fn_w_counter.caller_info


# Görseldeki Test Senaryoları
if __name__ == '__main__':
    # custom_power testleri
    assert custom_power(2) == 2
    assert custom_power(2, 3) == 8
    assert custom_power(2, e=2) == 4

    # custom_equation testleri
    assert custom_equation(2, 3) == 5.0
    assert custom_equation(2, 3, 2) == 7.0
    assert custom_equation(2, 3, 2, 3) == 31.0
    assert custom_equation(3, 5, a=2, b=3, c=4) == 33.5
    assert custom_equation(3, 5, 2, b=3, c=4) == 33.5
    assert custom_equation(3, 5, 2, 3, c=4) == 33.5

    # fn_w_counter testleri
    for i in range(10):
        fn_w_counter()
    
    assert fn_w_counter() == (11, {'__main__': 11})
    print("Tüm testler başarıyla geçildi!")
