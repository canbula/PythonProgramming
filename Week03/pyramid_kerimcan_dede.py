def calculate_pyramid_height(number_of_blocks):
    height = 0
    needed_block = 1
    while number_of_blocks >= needed_block:
        height = height + 1
        number_of_blocks = number_of_blocks - needed_block
        needed_block = needed_block + 1
    return height
