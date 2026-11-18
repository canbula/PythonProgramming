def remove_duplicates(seq: list) -> list:
    return list(set(seq))

def list_counts(seq: list) -> dict:
    dictionary = dict.fromkeys(seq, 0)
    for item in seq:
        dictionary[item] += 1
    return dictionary

def reverse_dict(d: dict) -> dict:
    new_dict = {}
    for key, value in d.items():
        new_dict[value] = key
    return new_dict
