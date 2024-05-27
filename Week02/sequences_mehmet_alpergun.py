my_list=[1,2,3,4,5]
my_tuple=(1,2,3,4,5)
my_set={1,2,3,4,5}
my_dict={'name':'Mehmet',
           'surname':'Alpergün',
           'Job':'Back-end Developer'}

def remove_duplicates(my_list):
    return list(set(my_list))

def list_counts(my_list):
    new_dict = dict()
    for item in my_list:
        if item  in new_dict:
            new_dict[item] = new_dict[item] + 1
        else:
            new_dict[item] = 1
    return new_dict

def reverse_dict(my_dict):
    new_dict = dict()
    for i,j in my_dict.items():
        new_dict[j] = i
    return new_dict
