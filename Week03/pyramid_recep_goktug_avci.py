def calculate_pyramid_height(number_of_blocks: int) -> int:
    height = 0 # Güncel height
    needed_blocks = 1 # o anki katmanda gereken blok sayısı
    while number_of_blocks >= needed_blocks:
        number_of_blocks -= needed_blocks
        height += 1
        needed_blocks += 1
    return height
