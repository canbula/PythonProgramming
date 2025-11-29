import math
def calculate_pyramid_height(number_of_blocks):
    if number_of_blocks <= 0:
       return 0
    height = (-1 + math.sqrt(1 + 8 * number_of_blocks)) / 2
    return math.ceil(height)
print(calculate_pyramid_height(11))
