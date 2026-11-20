def calculate_pyramid_height(number_of_blocks):
    height = 0
    needed_block = 1
    while number_of_blocks >= needed_block:
        number_of_blocks -= needed_block
        height += 1
        needed_block += 1
    return height
