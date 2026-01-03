def remove_duplicates(data):
    result = []
    for item in data:
        if item not in result:
            result.append(item)
    return result

def list_counts(data):
    counts = {}
    for item in data:
        counts[item] = counts.get(item, 0) + 1
    return counts

def reverse_dict(d):
    return {v: k for k, v in d.items()}
