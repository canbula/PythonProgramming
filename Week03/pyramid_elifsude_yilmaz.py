def calculate_pyramid_height(blocks):
    height = 0
    needed_for_next_level = 1
    
    while blocks >= needed_for_next_level:
        blocks -= needed_for_next_level
        height += 1
        needed_for_next_level += 1
        
    return height
