my_list = ["Mert", "Can", "Fidan", "Can", "Fidan",24,24,24]
my_tuple = ("Mert", "Can", "Fidan")
my_set = {"Mert", "Can", "Fidan"}
my_dictionary = {
  "name": "Mert Can Fidan",
  "age": 24,
  "alive": True
}

def remove_duplicates (any_list):
  return list(set(any_list))

# Simply creates an empty dictionary and copy of given list without duplicates of items. 
# After that checks item counts one byu one and adds to newly created dictionary.
def list_counts (any_list):
  empty_dict = {}
  for i in set(any_list): empty_dict[i] = any_list.count(i)
  return empty_dict

# Creates empty dictionary and switch rows in dictionary one by one with foor loop.
def reverse_dict (any_dict):
  empty_dict = {}
  for key,value in any_dict.items(): empty_dict[value] = key 
  return empty_dict
