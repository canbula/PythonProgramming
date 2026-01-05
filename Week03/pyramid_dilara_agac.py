def calculate_pyramid_height(number_of_blocks):
    """
    This function calculates the height of a pyramid
    that can be built with the given number of blocks.
    """
    height = 0
    used_blocks = 0

    while used_blocks + (height + 1) <= number_of_blocks:
        height += 1
        used_blocks += height

    return height
