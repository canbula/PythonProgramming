def remove_duplicates(seq: list) -> list:
    production = []
    for item in seq:
        if item not in production:
            production.append(item)
    return production

def list_counts(seq: list) -> dict:
    counts = {}
    for item in seq:
        counts[item] = counts.get(item, 0) + 1
    return counts

def reverse_dict(d: dict) -> dict:
    return {value: key for key, value in d.items()}
