my_list = [2, 2, 4, 4, 4, 6, 10, 14]
my_tuple = (1, 3, 'b', 9, 9)
my_set = {1, 2, 2, 2, 4, 8, 16, "apple", "apple"}
my_dict = {"name": "Zeynep",
           "department": "Computer Science",
           "gender": "female",
           "age:": "23"}

def remove_duplicates(my_list):
    new_list = list()
    for i in my_list:
        if i not in new_list:
            new_list.append(i)
    return new_list

def list_counts(my_list):
    counts = dict()
    for j in my_list:
        if j in counts:
            counts[j] += 1
        else:
            counts[j] = 1
    return counts

def reverse_dict(my_dict):
    reversed_dict = {}
    for key, value in my_dict.items():
        reversed_dict[value] = key
    return reversed_dict

