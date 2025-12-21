def remove_duplicates(seq: list) -> list:
    seen = set()
    result = []

    for item in seq:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result


def list_counts(seq: list) -> dict:
    counts = {}
    for item in seq:
        counts[item] = counts.get(item, 0) + 1
    return counts


def reverse_dict(d: dict) -> dict:
    reversed_d = {}

    for key, value in d.items():
        if value not in reversed_d:
            reversed_d[value] = key
        else:
            if isinstance(reversed_d[value], list):
                reversed_d[value].append(key)
            else:
                reversed_d[value] = [reversed_d[value], key]

    return reversed_d

if __name__ == "__main__":
    print(remove_duplicates([1, 2, 1, 3, 2, 4, 4]))
    print(list_counts(["a", "b", "a", "c", "b", "a"]))
    print(reverse_dict({"x": 1, "y": 2}))
    print(reverse_dict({"x": 1, "y": 1, "z": 2}))
