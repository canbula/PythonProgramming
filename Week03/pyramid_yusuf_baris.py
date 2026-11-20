def calculate_pyramid_height(number_of_blocks):
    height = 0
    blocks_used = 0
    while blocks_used + (height + 1) ** 2 <= number_of_blocks:
        height += 1
        blocks_used += height ** 2
    return height


print(calculate_pyramid_height(14)) 
