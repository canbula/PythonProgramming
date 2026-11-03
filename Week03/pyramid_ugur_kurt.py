def calculate_pyramid_height(number_of_blocks):
    height = 0
    block_needed = 1
    
    while number_of_blocks >= block_needed:
        number_of_blocks -= block_needed  
        height += 1                      
        block_needed += 1                 
        
    return height
