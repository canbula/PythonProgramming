def calculate_pyramid_height(block_count):
    
    height = 0
    used_blocks = 0
    
   
    while used_blocks + (height + 1) <= block_count:
      
        height = height+ 1
        used_blocks = used_blocks + height
            
    return height

# Function Test
sample_block_count = 16
result = calculate_pyramid_height(sample_block_count)
print(result)
