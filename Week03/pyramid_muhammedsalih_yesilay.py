def calculate_pyramid_height(number_of_blocks):
    height = 0

    for i in range(1, number_of_blocks + 1):
        if number_of_blocks >= i:
            number_of_blocks -= i
            height += 1
        else:
            break

    #print("Kalan blok sayısı:", number_of_blocks)
    return height
