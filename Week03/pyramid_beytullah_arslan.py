def calculate_pyramid_height(number_of_blocks):
    total = 0
    height = 0
    for i in range(1, number_of_blocks + 1):
        total += i
        if total > number_of_blocks:
            break
        else:
            height = i
    return height
