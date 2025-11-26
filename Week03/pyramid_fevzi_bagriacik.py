def calculate_pyramid_height(number_of_blocks):
    height = 0
    total = 0

    for i in range(1,number_of_blocks+2,1):

        total += i

        if number_of_blocks == total:
            height = i
            break
        elif number_of_blocks < total:
            height = i - 1
            break

        
    
    return height
