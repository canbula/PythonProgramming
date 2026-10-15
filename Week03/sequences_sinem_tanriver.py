from collections import Counter


def remove_duplicates(seq: list) -> list:
    """
    This function removes duplicates from a list.
    """
    seen = set()
    unique = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def list_counts(seq: list) -> dict:
    """
    This function counts the number of occurrences of each item in a list.
    """
    return dict(Counter(seq))


def reverse_dict(d: dict) -> dict:
    """
    This function reverses the keys and values of a dictionary.
    """
    return dict(zip(d.values(), d.keys()))
