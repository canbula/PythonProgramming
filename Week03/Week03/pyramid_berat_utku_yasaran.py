def calculate_pyramid(number_of_blocks: int) -> int:
     height = 0
     needed_blocks = 0
     while needed_blocks + height + 1 <= number_of_blocks:
         height += 1
         needed_blocks += height




     return height
