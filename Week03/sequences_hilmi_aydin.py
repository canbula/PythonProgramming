def remove_duplicates(seq: list) -> list:
    """
    This function removes duplicates from a list.
    """
    # Convert list to dictionary to remove duplicates, then back to list while preserving order
    return list(dict.fromkeys(seq))

def list_counts(seq: list) -> dict:
    """
    This function counts the number of occurrences of each item in a list.
    """
    counts = {}
    for item in seq:
        # If item exists, increment its count. Otherwise, default to 0 and add 1
        counts[item] = counts.get(item, 0) + 1
    return counts

def reverse_dict(d: dict) -> dict:
    """
    This function reverses the keys and values of a dictionary.
    """
    # Swap keys and values using dictionary comprehension
    return {value: key for key, value in d.items()}