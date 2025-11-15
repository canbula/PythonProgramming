import math

def calculate_square_pyramid_properties(base_edge, height):
    base_area = base_edge ** 2
    half_base = base_edge / 2
    
    slant_height = math.sqrt(height**2 + half_base**2)
    
    lateral_edge_length = math.sqrt(height**2 + (base_edge**2) / 2)
    
    volume = (1/3) * base_area * height
    
    # Yanal Alan (Lateral Surface Area)
    # 4 * (bir üçgenin alanı) = 4 * (1/2 * taban_kenari * yan_yuzey_yuksekligi)
    lateral_surface_area = 2 * base_edge * slant_height
    
    total_surface_area = base_area + lateral_surface_area
    
    return {
        "Giriş (Taban Kenarı)": base_edge,
        "Giriş (Yükseklik)": height,
        "Hesaplanan (Yan Yüzey Yüksekliği)": slant_height,
        "Hesaplanan (Yan Ayrıt Uzunluğu)": lateral_edge_length,
        "Taban Alanı": base_area,
        "Yanal Alan": lateral_surface_area,
        "Toplam Yüzey Alanı": total_surface_area,
        "Hacim": volume
    }
if __name__ == "__main__":
    try:
        a = float(input("Piramidin taban kenar uzunluğunu girin (a): "))
        h = float(input("Piramidin yüksekliğini girin (h): "))
        
        if a <= 0 or h <= 0:
            print("\nHata: Uzunluklar pozitif bir değer olmalıdır.")
        else:
            properties = calculate_square_pyramid_properties(a, h)
            print("\n--- Kare Piramit Hesaplama Sonuçları ---")
            for key, value in properties.items():
                print(f"{key:<35}: {value:.4f}") 

    except ValueError:
        print("\nHata: Geçersiz bir sayı girdiniz. Lütfen sayısal bir değer girin.")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
