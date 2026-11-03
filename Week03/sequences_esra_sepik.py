def remove_duplicates(seq: list) -> list:
    """
    This function removes duplicates from a list.
    """
    return list(dict.fromkeys(seq))


def list_counts(seq: list) -> dict:
    """
    This function counts the number of occurrences of each item in a list.
    """
    return {item: seq.count(item) for item in seq}


def reverse_dict(d: dict) -> dict:
    """
    This function reverses the keys and values of a dictionary.
    """
    reversed_d = {}
    for key, value in d.items():
        reversed_d[value] = key
    return reversed_d
