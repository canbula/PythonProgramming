def remove_duplicates(lst):
    result = []
    seen = set()
    for x in lst:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result


def list_counts(lst):
    counts = {}
    for x in lst:
        counts[x] = counts.get(x, 0) + 1
    return counts


def reverse_dict(d):
    return {v: k for k, v in d.items()}
