def calculate_pyramid_height(number_of_blocks):
    height = 0
    layer_blocks = 1
    
    while number_of_blocks >= layer_blocks:
        number_of_blocks = number_of_blocks - layer_blocks
        height = height + 1
        layer_blocks = layer_blocks + 1
    return height