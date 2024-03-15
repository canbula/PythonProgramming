my_list = [2,3,3,3,3,3,3,3,3,3,3,3,3,2,1,4,5,6,7,8,9]
my_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
my_set = {"blossom", "bubbles", "buttercup"}
my_dict = {
    "Name" : "harry",
    "Surname" : "potter" ,
    "job" : "student" ,
    "location" : "hogwarts",
    "age" : 16}

def remove_duplicates(my_list):
    new_list = []
    for i in my_list:
        if i not in new_list:
            new_list.append(i)
    return new_list  


def list_counts(my_list):
    return {i : my_list.count(i) for i in my_list} 


def reverse_dict(my_dict):
    reversed_dict = {}
    for key,value in my_dict.items():
        reversed_dict[value] = key
    return reversed_dict  
