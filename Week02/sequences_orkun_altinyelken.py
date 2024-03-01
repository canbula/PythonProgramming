my_list = ["Ataturk", "a", "b", "c", "c", "a", "a"]
my_tuple = (1, 2, 3)
my_set = {"Emma D'Arcy", "Matt Smith", "Paddy Considine"}
my_dict = {'Name': "Acheron", "Occupation": "Galaxy Ranger", "Birth Year": "???"}


def remove_duplicates(my_list):
    return list(set(my_list))


def list_counts(the_list):
    counted = {}
    for element in the_list:
        counted[element] = counted.get(element, 0) + 1
    return counted


def reverse_dict(dictionary):
    dictionary = {v: k for k, v in dictionary.items()}
    return dictionary
