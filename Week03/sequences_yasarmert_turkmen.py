def remove_duplicates(seq: list) -> list:
    a_list = []
    for i in seq:
        if i not in a_list:
            a_list.append(i)
    return a_list

def list_counts(seq: list) -> dict:
    a_dict = {}
    for i in seq:
        a_dict[i] = seq.count(i)
    return a_dict

def reverse_dict(d: dict) -> dict:
    a_dict = {}
    for key, value in d.items():
        a_dict[value] = key
    return a_dict
