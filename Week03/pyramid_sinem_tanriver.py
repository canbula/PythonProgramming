def calculate_pyramid_height(number_of_blocks):
    height = 0
    for row in range(1, number_of_blocks + 1):
        if number_of_blocks < row:
            break
        number_of_blocks -= row
        height += 1
    return height
