def remove_duplicates(seq: list) -> list:
    unique_items = []
    for element in seq:
        if element not in unique_items:
            unique_items.append(element)
    return unique_items


def list_counts(seq: list) -> dict:
    frequencies = {}
    for element in seq:
        if element in frequencies:
            frequencies[element] += 1
        else:
            frequencies[element] = 1
    return frequencies


def reverse_dict(d: dict) -> dict:
    inverted = {}
    for k, v in d.items():
        inverted[v] = k
    return inverted