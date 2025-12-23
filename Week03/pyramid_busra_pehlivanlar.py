def calculate_pyramid_height(number_of_blocks):
    height = 0
    needed_for_next_level = 1
    while number_of_blocks >= needed_for_next_level:
        number_of_blocks -= needed_for_next_level
        height += 1
        needed_for_next_level += 1
        
    return height
