def calculate_pyramid_height(n):
    h = 0
    while (h + 1) * (h + 2) // 2 <= n:
        h += 1
    return h
