
my_list = ["Raw Prime Meat", True , 211, "Saddle"]
my_tuple = "Rex","Pterenadon",215,False,("Raptor","Microraptor")
my_dictionary = {"Narcotic" :" a tranquilizer", "duration_in_minute":10,}
my_set = set(["42",64,"sdad","sad",64,42]) #duplicated values will be removed


def remove_duplicates(my_list_):
    #We shouldn't use sets for this method, because sets are unordered and if we use
    # sets, our list will no longer be ordered, it will be random ordered.
    non_duplicated_list = []
    for item in my_list_:
        if item not in non_duplicated_list:
            non_duplicated_list.append(item)

    return non_duplicated_list


def list_counts(my_list_):
    count_dictionary= {}

    for item in my_list_:
        if item not in count_dictionary:
            count_dictionary[item] = 1
        else:
            count_dictionary[item] += 1

    return count_dictionary

def reverse_dict(dict):
    #!!! If there are identical keys in dictionary, when they reversed, if they are integer
    #    the result will be sum of those integer but if they are string, then
    #    the result will be the last selected item.
    reversed_dict = {}

    for item in dict:
        reversed_dict[dict[item]] = item

    return reversed_dict

