def calculate_pyramid_height(number_of_blocks):
    height = 0
    used = 1
    while number_of_blocks >= used:
        number_of_blocks -= used
        height += 1
        used += 1
    return height
