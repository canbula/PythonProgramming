def remove_duplicates(lst: list) -> list:
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
    
def list_counts(lst: list) -> dict:
    counts = {}
    for item in lst:
        counts[item] = counts.get(item, 0) + 1
    return counts    

def reverse_dictionary(d: dict) -> dict:
    return {v: k for k, v in d.items()}
