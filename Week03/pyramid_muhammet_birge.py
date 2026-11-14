
def calculate_pyramid_height(number_of_blocks):
    height = 0
    used_blocks = 0

    while True:
        required_blocks = height + 1

        if used_blocks + required_blocks > number_of_blocks:
            break

        used_blocks += required_blocks
        height += 1

    return height
