def calculate_pyramid_height(number_of_blocks):
    height = 0 
    blocks_used = 0
    counter = 1
    while blocks_used < number_of_blocks:
        blocks_used += counter 
        if blocks_used == number_of_blocks:
            height = counter
            break
        elif blocks_used > number_of_blocks:
            height = counter - 1
            break
        counter += 1     
    return height


if __name__ == "__main__":
    print(calculate_pyramid_height(1))
    print(calculate_pyramid_height(2))
    print(calculate_pyramid_height(6))
    print(calculate_pyramid_height(20))
    print(calculate_pyramid_height(100))
    print(calculate_pyramid_height(1000))
    print(calculate_pyramid_height(10000))
    print(calculate_pyramid_height(100000))