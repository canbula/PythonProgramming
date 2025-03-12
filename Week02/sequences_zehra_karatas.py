my_list = [1, 2, 3, 3, 1, 1, 4]
my_tuple = (2, 4, 4, 7, 9) 
my_set = {3, 10, 12, 15, 19} 
my_dict = {
  "first_exam" : 67,
  "second_exam" : 89,
  "third_exam" : 58
}


def remove_duplicates(my_list):
  update_list = list(set(my_list))
  return update_list


def list_counts(my_list):
  counts = {} #empty dict
  for item in my_list:
    if item in counts:
      counts[item] += 1
    else:
      counts[item] = 1
  return counts


def reverse_dict(my_dict):
  reverse_dict = {}
  for key, value in my_dict.items():
    reverse_dict[value] = key
  return reverse_dict
  
  
result_duplicates = remove_duplicates(my_list)  
result_counts= list_counts(my_list)
result_reverse = reverse_dict(my_dict)

print(result_duplicates)
print(result_counts)
print(result_reverse)



      
      
