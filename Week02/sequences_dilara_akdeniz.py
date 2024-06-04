my_list = [1,2,3,4,5,6,6,6]

my_tuple = (6,7,8,9,6,7)

my_set = {3,5,7}

my_dict = { "name" : "Dilara", "surname" : "Akdeniz"}

def remove_duplicates(my_list):
  return list(set(my_list))

def list_counts(my_list) -> dict:
  new_dict = {}
  for item in my_list:
    if item in new_dict:
      new_dict[item] += 1
    else:
      new_dict[item] = 1
  return new_dict

def reverse_dict(my_dict) -> dict:
  new_dict = {}
  for key, value in my_dict.items():
    new_dict[value] = key
  return new_dict
