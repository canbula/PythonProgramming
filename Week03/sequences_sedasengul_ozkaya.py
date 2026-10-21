def remove_duplicates(items):
    return list(dict.fromkeys(items))


def list_counts(items):
    counts = {}

    for item in items:
        counts[item] = counts.get(item, 0) + 1

    return counts


def reverse_dict(dictionary):
    reversed_dict = {}

    for key, value in dictionary.items():
        reversed_dict[value] = key

    return reversed_dict
