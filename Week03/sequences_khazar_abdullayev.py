def remove_duplicates(seq: list) -> list:
    seq.sort()
    i = 1
    while i < len(seq):
        if seq[i] == seq[i - 1]:
            seq.pop(i)
        else:
            i = i + 1
            
    return seq

def list_counts(seq: list) -> dict:
    seq.sort()
    counts = {}
    for item in seq:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts
    
def reverse_dict(d: dict) -> dict:
    d_reverse = {}
    for key in d:
        value = d[key]
        d_reverse[value] = key
        
    return d_reverse