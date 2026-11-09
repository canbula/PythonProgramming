def remove_duplicates(seq: list) -> list:
    """
    Remove duplicates from a list while preserving the order of elements.

    Args:
        seq (list): The input list from which duplicates need to be removed.

    Returns:
        list: A new list containing only unique elements from the input list.
    """
    seen = set()
    result = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def list_counts(seq: list) -> dict:
    """
    Count the occurrences of each element in a list.

    Args:
        seq (list): The input list for which counts need to be calculated.

    Returns:
        dict: A dictionary where keys are unique elements from the list and values are their respective counts.
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
    Reverse the keys and values of a dictionary.

    Args:
        d (dict): The input dictionary to be reversed.

    Returns:
        dict: A new dictionary with keys and values swapped.
    """
    return {v: k for k, v in d.items()}
