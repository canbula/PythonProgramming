def calculate_pyramid_height(number_of_blocks):
    height = 0
    blocks = 0

    while blocks + height + 1 <= number_of_blocks:
        height += 1
        blocks += height

    return height
