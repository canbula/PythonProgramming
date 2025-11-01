def remove_duplicates(seq: list) -> list:
    return list(dict.fromkeys(seq))

def list_counts(seq: list) -> dict:
    counts = {}
    for item in seq:
        counts[item] = counts.get(item, 0) + 1
    return counts

def reverse_dict(d: dict) -> dict:
    return {value: key for key, value in d.items()}

sample_list = [1, 2, 2, 3, 4, 4, 5]
sample_dict = {'a': 1, 'b': 2, 'c': 3}

print("Original list:", sample_list)
print("List after removing duplicates:", remove_duplicates(sample_list))
print("Counts of each element in the list:", list_counts(sample_list))
print("Original dictionary:", sample_dict)
print("Reversed dictionary:", reverse_dict(sample_dict))
