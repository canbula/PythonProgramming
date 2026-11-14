def calculate_pyramid_height(number_of_blocks):
    """Return the height of the pyramid that can be built with the given blocks.

    Each level i needs i blocks (1 on top, 2 below it, and so on).
    """
    height = 0
    while number_of_blocks >= height + 1:
        height += 1
        number_of_blocks -= height
    return height
