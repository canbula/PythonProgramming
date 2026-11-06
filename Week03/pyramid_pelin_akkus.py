def calculate_pyramid_height(number_of_blocks):
  height=0
  #block control
  while number_of_blocks >= height +1:
    height += 1
    number_of_blocks -= height
  return height 
