def calculate_pyramid_height(number_of_blocks):
    """
    This function calculates the height of a pyramid
    given the number of blocks available.
    
    A pyramid has 1 block at top, 2 blocks in second row,
    3 blocks in third row, etc.
    
    Returns the maximum height that can be built.
    """
    height = 0
    total_blocks_used = 0
    
    while total_blocks_used + (height + 1) <= number_of_blocks:
        height += 1
        total_blocks_used += height
    
    return height
