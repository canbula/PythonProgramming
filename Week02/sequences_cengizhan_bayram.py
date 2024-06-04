my_list = [1, 2, 3, 3, 5, 7]
my_tuple = (3, 6, 9, 9, 8, 7, 4, 5, 4)
my_set = {8, 7, 8, 7, 8, 9, 1}
my_dict = {
    "name": "Ezio ",
    "surname": "auditore",
    "city": "QONYA",
    "age": 22
}

def remove_duplicates(my_list):
    return list(set(my_list))

def list_counts(my_list):
    counts = {}
    for item in my_list:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts

def reverse_dict(dictionary):
    return {value: key for key, value in dictionary.items()}