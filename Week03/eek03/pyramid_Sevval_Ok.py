def calculate_pyramid_height(number_of_blocks: int) -> int:
    
    if number_of_blocks <= 0:
        return 0

    height = 0
    used = 0
  
    while True:
        next_level = height + 1
        if used + next_level > number_of_blocks:
            break
        used += next_level
        height += 1

    return height

if __name__ == "__main__":
    tests = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 15]
    for n in tests:
        print(n, "->", calculate_pyramid_height(n))
