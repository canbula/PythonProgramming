my_list = ["wasd", 123, True, True, "qwer", [456, "zxcv"]] #mutable
my_tuple = "wasd", 123, True, True, "qwer", (456, "zxcv")  #immutable
my_set = {"wasd", 123, True, True, "qwer", (456, "zxcv")}  #will be no duplicates
my_dict = {1: 5, "secondKey: ": 6, "thirdKey: ": "seven"}

def remove_duplicates(a_list):
    list_no_duplicates = []
    for item in a_list:
        if item not in list_no_duplicates:
            list_no_duplicates.append(item)

    return list_no_duplicates

def list_counts(a_list):
    counted_dict = {}
    for item in a_list:
        if item not in counted_dict:
            counted_dict[item] = 1
        else:
            counted_dict[item] += 1

    return counted_dict

def reverse_dict(a_dict):
    reversed_dict = {}
    for item in a_dict:
        reversed_dict[a_dict[item]] = item

    return reversed_dict
