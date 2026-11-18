def remove_duplicates(seq: list) -> list:
    new_list = []
    for i in seq:
        if i not in new_list:
            new_list.append(i)
    return new_list

def list_counts(seq: list) -> dict:
    result_dict = dict.fromkeys(seq, 0)
    for i in seq:
        result_dict[i] = result_dict[i] + 1
    return result_dict

def reverse_dict(d: dict) -> dict:
    new_dict = {}
    for key, value in d.items():
        new_dict[value] = key
    return new_dict
