my_list = [1, 5, 8, "x", 9]
my_tuple = (7, 4, 1)
my_set = {3, 5, 7}
my_dict = {"name":"İrem", "surname":"Köse", "age":23}

def remove_duplicates(a_list):
    return list(set(a_list))

def list_counts(a_list):
    a_dict = {}
    for  i in a_list:
        if i not in a_dict :
            a_dict[i]=1
        else:
            a_dict[i]+=1
    return a_dict

def reverse_dict(a_dict):
    new_dict = {}
    for key, value in a_dict.items():
        new_dict[value] = key
    return new_dict
