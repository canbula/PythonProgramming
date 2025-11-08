def remove_duplicates(seq: list) -> list:
    seen = set()
    result = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            result.append(item)
    seq.clear()
    seq = result.copy()
    return seq

def list_counts(seq: list) -> dict:
    counts = {}
    for item in seq:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts

def reverse_dict(d: dict) -> dict:
    reversed_dict = {}
    for key, value in d.items():
        if value in reversed_dict:
            reversed_dict[value].append(key)
        else:
            reversed_dict[value] = [key]
    d.clear()
    d.update(reversed_dict)
    return d

if __name__ == "__main__":
    print(remove_duplicates([1, 1, 2, 3, 3, 4, 4, 5, 5,5, 5, 5, 6]))
    print(list_counts([1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 6,6]))
    print(reverse_dict({'a': 1, 'b': 2, 'c': 1, 'd': 3}))
