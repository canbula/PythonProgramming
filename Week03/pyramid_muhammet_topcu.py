def calculate_pyramid_height(n: int) -> int:
    h = 0
    used = 0
    while used + h + 1 <= n:
        h += 1
        used += h
    return h
