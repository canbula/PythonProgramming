my_list = [1,2,3]

my_tuple = ("tuple1","tuple2")

my_set = {1,1,2,2,3,3,4,5}

my_dict = {"name" : "Burak" , "surname" : "Memis"}

def remove_duplicates(list):
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
