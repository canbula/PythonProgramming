def remove_duplicates(seq: list) -> list:
    """
    This function removes duplicates from a list.
    """
    result = []
    for item in seq:
        if item not in result:
            result.append(item)
    return result


def list_counts(seq: list) -> dict:
    """
    This function counts the number of
    occurrences of each item in a list.
    """
    counts = {}
    for item in seq:
        counts[item] = counts.get(item, 0) + 1
    return counts


def reverse_dict(d: dict) -> dict:
    """
    This function reverses the keys
    and values of a dictionary.
    """
    reversed_d = {}
    for k, v in d.items():
        reversed_d[v] = k
    return reversed_d
