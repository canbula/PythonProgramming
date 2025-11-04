input_Cube_number = int(input("number of cubes : "))

def calculate_pyramid_height(number_of_blocks):
    piramit_cube_height = 1
    cube_number_of_piramit = 0

    while True:
      if cube_number_of_piramit > number_of_blocks:
         break
      cube_number_of_piramit += piramit_cube_height
      piramit_cube_height += 1
      
    piramit_cube_height -= 2
    print("the height of the piramit is : ", piramit_cube_height) 
    return piramit_cube_height

calculate_pyramid_height(input_Cube_number)
