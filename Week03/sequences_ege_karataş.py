def remove_duplicates(seq: list) -> list:
    result = []
    for i in seq:
        if i not in result:
            result.append(i)
    return result

def list_counts(seq: list) -> dict:
    counts = {}
    for i in seq:
        counts[i] = counts.get(i, 0) + 1
    return counts

def reverse_dict(d: dict) -> dict:
    result = {}
    for key, value in d.items():
        result[value] = key
    return result
