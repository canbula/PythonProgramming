def remove_duplicates(seq: list) -> list:
    """
    Remove repeated elements from a list.
    """
    unique_items = []

    for value in seq:
        if value not in unique_items:
            unique_items.append(value)

    return unique_items


def list_counts(seq: list) -> dict:
    """
    Count how many times each element appears in a list.
    """
    result = {}

    for value in seq:
        if value in result:
            result[value] += 1
        else:
            result[value] = 1

    return result


def reverse_dict(d: dict) -> dict:
    """
    Exchange the keys and values of a dictionary.
    """
    reversed_dict = {}

    for key, value in d.items():
        reversed_dict[value] = key

    return reversed_dict
