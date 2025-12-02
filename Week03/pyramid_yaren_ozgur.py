def calculate_pyramid_height(number_of_blocks):
    height = 0
    used = 0
    while used + (height + 1) <= number_of_blocks:
        height += 1
        used += height
    return height
