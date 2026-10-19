def calculate_pyramid_height(number_of_blocks):
    height = 0
    block_needed = 1


    while number_of_blocks >= block_needed:
        block_needed += 1
        height += 1
        number_of_blocks -= block_needed
        
    return height
