def remove_duplicates(seq: list) -> list:
    """
    Remove duplicate elements from a list while preserving the original order.
    Only the first occurrence of each element is kept.
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
    Count how many times each element appears in a list.
    Returns a dictionary where keys are elements and values are counts.
    """
    counts = {}
    for item in seq:
        counts[item] = counts.get(item, 0) + 1
    return counts


def reverse_dict(d: dict) -> dict:
    """
    Reverse the keys and values of a dictionary.
    If multiple keys have the same value, the last one overwrites the earlier ones.
    """
    reversed_dict = {}
    for key, value in d.items():
        reversed_dict[value] = key
    return reversed_dict
