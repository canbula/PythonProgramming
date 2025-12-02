from typing import List, Dict, Any

def remove_duplicates(seq: List) -> List:
    seen = set()
    result = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def list_counts(seq: List) -> Dict
    counts = {}
    for item in seq:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts

def reverse_dict(d: Dict) -> Dict:
    reversed_d = {}
    for key, value in d.items():
        reversed_d[value] = key
    return reversed_d

