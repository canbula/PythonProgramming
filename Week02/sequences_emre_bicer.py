my_list = []
my_tuple = ()
my_set = set()
my_dict = {}


def remove_duplicates(list_):
    temp_set = set(list_)
    new_list = list(temp_set)
    return new_list


def list_counts(list_):
    new_list = []
    list_length = len(list_)
    counted_elements = []

    for i in range(list_length):
        if i not in counted_elements:
            counted_elements.append(i)
            element = list_[i]
            elementCount = list_.count(element)
            new_list.append((element, elementCount))
    
    return dict(new_list)


def reverse_dict(dict_):
    new_dict = {}

    for k,v in dict_.items():
        new_dict[v] = k
    
    return new_dict
