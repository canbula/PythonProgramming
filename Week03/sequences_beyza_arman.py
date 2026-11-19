def remove_duplicates(items):
    """Remove duplicates while preserving the first occurrence order."""
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def list_counts(items):
    """Return the frequency of each item."""
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


def reverse_dict(mapping):
    """Swap keys and values; the last key wins for repeated values."""
    return {value: key for key, value in mapping.items()}
