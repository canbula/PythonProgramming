import collections

def remove_duplicates(seq: list) -> list:
    """This function removes duplicates from a list."""
    return sorted(set(seq), key=seq.index)

def list_counts(seq: list) -> dict:
    """This function counts the number of occurrences of each item in a list."""
    return dict(collections.Counter(seq))

def reverse_dict(d: dict) -> dict:
    """This function reverses the keys and values of a dictionary."""
    return dict(zip(d.values(), d.keys()))
