def calculate_pyramid_height(number_of_blocks):
    height = 0 
    block_number = 1

    while number_of_blocks >= block_number:
        number_of_blocks = number_of_blocks - block_number
        height = height +1
        block_number = block_number +1
    
    return height    

result = calculate_pyramid_height(9)
print(result)
