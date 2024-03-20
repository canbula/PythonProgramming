my_list=[7, 9 , 11, 11 , 12, 17, 17, 25]
my_tuple=(1, 2 ,3 ,4 ,5)
my_set={"gta5", "watchdogs", "eycofcu1"}
my_dict={"Name" : "Umit", "Surname" : "UNAL", "Age" : 23}

def remove_duplicates(my_list):
    return list(set(my_list))

def list_counts(my_list):
    counts = {}
    for i in my_list:
        if i in counts:
            counts[i] += 1
        else:
            counts[i] = 1
    return counts

def reverse_dict(my_dict):
    reversed_dict = {}
    for key, value in my_dict.items():
        reversed_dict[value] = key
    return reversed_dict

