def calculate_pyramid_height(number_of_blocks):
    height = 0
    needed_blocks = 1

    while needed_blocks <= number_of_blocks:
        height = height + 1
        number_of_blocks = number_of_blocks - needed_blocks
        needed_blocks = needed_blocks + 1

    return height
