def remove_duplicates(seq: list) -> list:
    """Return a new list without duplicates, keeping the original order."""
    result = []
    for item in seq:
        if item not in result:
            result.append(item)
    return result


def list_counts(seq: list) -> dict:
    """Return a dictionary with the number of occurrences of each item."""
    counts = {}
    for item in seq:
        counts[item] = counts.get(item, 0) + 1
    return counts


def reverse_dict(d: dict) -> dict:
    """Return a dictionary with keys and values swapped."""
    return {value: key for key, value in d.items()}
