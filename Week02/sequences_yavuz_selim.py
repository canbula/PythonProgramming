my_list = [1,"Y",False,3.2,False]
my_tuple = (5,13,36)
my_set = {3,5,"hi",7,5}
my_dict =  { "a": 100, "b":"B","c":True }

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
    key_list = a_dict.keys()
    value_list = a_dict.values()
    new_dict = dict.fromkeys(value_list,key_list)
    return new_dict
