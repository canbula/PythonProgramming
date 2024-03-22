my_list = [1, 2, 3, 3, 4, 5, 5, 5, 6]
my_tuple = (1, 2, 3, 4, 5)
my_set = {1, 2, 3, 4, 5}
my_dict = {'a': 1, 'b': 2, 'c': 3}

def remove_duplicates(seq):
    return list(set(seq))

def list_counts(seq):
    counts = {}
    for item in seq:
        counts[item] = counts.get(item, 0) + 1
    return counts

def reverse_dict(d):
    return {v: k for k, v in d.items()}
