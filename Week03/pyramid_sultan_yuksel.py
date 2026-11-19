def calculate_pyramid_height(number_of_blocks):
  height = 0     # Inıtıal height
  needed_blocks = 1  # Number of blocks required inıtıally
  while number_of_blocks >= needed_blocks:
    number_of_blocks -= 1
    height += 1
    needed_blocks += 1
  return height
