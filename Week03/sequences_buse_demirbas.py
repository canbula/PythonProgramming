def remove_duplicates(seq : list) -> list:
    new_items = set(seq)
    return list(new_items)
def list_counts(seq : list) -> dict:
    counts = {}
    for item in seq:
        counts[item] = counts.get(item , 0) +1
        return counts
def reverse_dict(d : dict) -> dict:     
    result = {}
    for key , value in d.items():
        result[value] = key
    return result
