def calculate_pyramid_height(number_of_blocks):
    height = 0
    required_block = 1  

    while number_of_blocks >= required_block:
        number_of_blocks -= required_block
        height += 1
        required_block += 1  

    return height
