from collections import Counter

my_list = [1,1,2,3,5,8,13,13,13]
my_tuple = [20,21,22,23,24,25]
my_set = [1,2,2,3,3,3,4,4,4,4,5,5,5,5,5]
my_dict = {'a': 1, 'b': 2, 'c': 3}

def remove_duplications(liste):
  remove_dup = list(set(my_list))
  return remove_dup


def reverse_dict(d):
    return {v: k for k, v in d.items()}
from collections import Counter


def list_counts(lst):
    return dict(Counter(lst))


print(remove_duplications(my_list))  
print(list_counts(my_list))

reversed_dict = reverse_dict(my_dict)
print(reversed_dict)
