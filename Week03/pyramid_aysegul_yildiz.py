def calculate_pyramid_height(number_of_blocks):
    height = 0
    used_blocks = 0

    for level in range(1, number_of_blocks + 1):
        # Taş ihtiyacı: level*(level+1)/2
        blocks_needed = level * (level + 1) // 2

        if used_blocks + blocks_needed > number_of_blocks:
            break

        used_blocks += blocks_needed
        height = level

    return height
