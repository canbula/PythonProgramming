def remove_duplicates(seq: list) -> list:
    result = []
    for item in seq:
        if item not in result:
            result.append(item)
    return result
  
def list_counts(seq: list) -> dict:
    counts = {}
    for item in seq:
        counts[item] = counts.get(item, 0) + 1
    return counts
  
def reverse_dict(d: dict) -> dict:
    reversed_d = {}
    for key, value in d.items():
        if value not in reversed_d:
            reversed_d[value] = [key]
        else:
            reversed_d[value].append(key)
    return reversed_d
