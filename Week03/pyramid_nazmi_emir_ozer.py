def calculate_pyramid_height(number_of_blocks):
    height = 0
    blocks_used=1

    while number_of_blocks >= blocks_used:
        number_of_blocks -= blocks_used
        height += 1
        blocks_used += 1
    return height
