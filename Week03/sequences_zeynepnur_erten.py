def remove_duplicates(seq: list) -> list:
    unique_list = []
    for i in seq:
        if i not in unique_list:
            unique_list.append(i)

    return unique_list


def list_counts(seq: list) -> dict:
    items = dict()
    for i in seq:
        if i not in items:
            items[i] = 1
        else:
            items[i] += 1

    return items
  

def reverse_dict(d: dict) -> dict:
    reversed_dict = {}
    for i in d:
        reversed_dict[d[i]] = i

    return reversed_dict





















