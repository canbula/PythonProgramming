def remove_duplicates(seq: list) -> list:
    """
    This function removes duplicates from a list
    """
    result = []
    for item in seq:
        if item not in result:
            result.append(item)
    return result


def list_counts(seq: list) -> dict:
    """
    This function counts the number of occurences
    of each item in a list
    """
    counts = {}
    for item in seq:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts


def reverse_dict(d: dict) -> dict:
    """
    This function reverses the keys and values
    of a dictionary
    """
    new_d = {}
    for key, value in d.items():
        new_d[value] = key
    return new_d