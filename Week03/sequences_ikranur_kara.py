def remove_duplicates(seq: list) -> list:
    res = []
    for item in seq:
        if item not in res:
            res.append(item)
    return res


def list_counts(seq: list) -> dict:
    counts = {}
    for item in seq:
        counts[item] = counts.get(item, 0) + 1
    return counts


def reverse_dict(d: dict) -> dict:
    return {v: k for k, v in d.items()}
