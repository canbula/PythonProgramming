def calculate_pyramid_height(number_of_blocks):

    height = 1

    while number_of_blocks >= height:

        number_of_blocks = number_of_blocks - height

        height = height + 1

    return height
