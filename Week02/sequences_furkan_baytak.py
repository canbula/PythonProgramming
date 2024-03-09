# Creating a list, tuple, set and dictionary
my_list = [1, 2, 3, 4, 5]
my_tuple = (1, 2, 3, 4, 5)
my_set = {1, 2, 3, 4, 5}
my_dict = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}


# Remove duplicate items from a list
def remove_duplicates(list_):
    return list(set(list_))


# Count the occurence of each item in a list and return as a dictionary
def list_counts(list_):
    return {i: list_.count(i) for i in list_}


# Reverse a dictionary, switch values and keys with each other
def reverse_dict(dict_):
    return {v: k for k, v in dict_.items()}
