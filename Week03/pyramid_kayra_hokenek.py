def calculate_pyramid_height(number_of_blocks):
    height = 0
    floor_blocks = 1

    while number_of_blocks >= floor_blocks:
        height += 1
        number_of_blocks -= floor_blocks
        floor_blocks += 1

    return height
