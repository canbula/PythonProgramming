def calculate_pyramid_height(number_of_blocks):
    height = 0
    blocks_used = 0
    next_row = 1

    while blocks_used + next_row <= number_of_blocks:
        blocks_used += next_row
        height += 1
        next_row += 1

    return height
