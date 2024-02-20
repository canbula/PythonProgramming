from collections import OrderedDict
from collections import Counter

my_list = ["Atatürk", "a","b","c","c","a","a"]
my_tuple = (1, 2, 3)
my_set = {"Emma D'Arcy", "Matt Smith", "Paddy Considine"}
my_dict = {'name': "Acheron", "Occupation": "Galaxy Ranger", "birth_year": "???"}
def remove_duplicates(my_list):
    return list(set(my_list))

def list_counter(list):
    return Counter(list)

def reverse_dict(dictionary):
    res = OrderedDict(reversed(list(dictionary.items())))
    return res


print(list_counter(my_list))
print(remove_duplicates(my_list))
print(reverse_dict(my_dict))
