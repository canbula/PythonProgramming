import math

def calculate_pyramid_height(n: int) -> int:
    if n <= 0:
        return 0

    # h(h+1)/2 <= n → h ≤ (sqrt(1 + 8*n) - 1) / 2
    
    h = (math.isqrt(1 + 8*n) - 1) // 2
    return int(h)

