def remove_duplicates(seq: list) -> list:
    no_duplicates = []
    for item in seq:
        if item not in no_duplicates:
            no_duplicates.append(item)

    return no_duplicates


def list_counts(seq: list) -> dict:
    d = {}
    for item in seq:
        if item not in d:
            d[item] = 1
        else:
            d[item] += 1
    return d

def reverse_dict(d: dict) -> dict:
    return {v: k for k, v in d.items()}
