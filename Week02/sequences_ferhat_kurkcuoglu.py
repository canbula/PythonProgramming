my_list = [3, 4, 5, 6, 9, 8, 3, 9, 10, 11, 3, 6]
my_tuple = (1, 3, 5, 7, 8, 9)
my_set = {5, 6, 7, 8, 9, 0}
my_dict = {"name": "Ferhat", "surname": "Kurkcuoglu", "age": 23}

def remove_duplicates(my_list) -> list:

    return list(set(my_list))
  

def list_counts(my_list) -> dict:
    count = dict()
    for i in my_list:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1
    return count


def reverse_dict(my_dict) -> dict:
    reversed_dict = dict()
    for k,v in my_dict.items():
        reversed_dict[v] = k
    return reversed_dict
