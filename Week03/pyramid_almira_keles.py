from __future__ import annotations

def calculate_pyramid_height(number_of_blocks: int) -> int:

    if number_of_blocks <= 0:
        return 0


    h = 0
    used = 0
    next_row = 1

    while used + next_row <= number_of_blocks:
        used += next_row
        h += 1
        next_row += 1

    return h
