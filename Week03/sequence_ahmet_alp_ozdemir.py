def remove_duplicates(seq):
    result = []
    for word in seq:
        if word not in result:
            result.append(word)
    return result


def list_counts(seq):
    counts = {}
    for word in seq:
        counts[word] = counts.get(word, 0) + 1
    return counts


def reverse_dict(d):
    reversed_str = {}
    for key, value in d.items():
        reversed_str[value] = key
    return reversed_str
