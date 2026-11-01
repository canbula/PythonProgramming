def remove_duplicates(seq: list) -> list:
    production = []
    for item in seq:
        if item not in production:
            production.append(item)
    return production

def list_count(seq: list) -> dict:
    count = {}
    for item in seq:
        count[item] = count.get(item, 0) + 1
    return count

def reverse_dict(d: dict) -> dict:
    return {value: key for key, value in d.items()}
