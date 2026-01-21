def remove_dublucates(seq: list) -> list:
    "bu fonksiyon bir listeden tektarları kaldır."
    new_list = []
    for item in seq:
        if item not in new_list:
            new_list.append(item)
    return new_list

print (remove_dublucates([1, 2, 4, 4, 7, 2, 3, 4, 5, 6, 7, 8, 9]))

def list_counts(seq: list) -> dict:
    "bu fonksiyon, bir listedeki her bir öğenin kaç kez görüldüğünü sayar"
    counts = {}
    for item in seq:
        if item in  counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts

print (list_counts([1, 2, 4, 4, 7, 2, 3, 4, 5, 6, 7, 8, 9]))

def reserve_dict(d: dict) -> dict:
    "bu fonksiyon bir sözcüğün anahtarlarını ve değerlerini tersine çevirir."
    new_dict = {}
    for key, value in d.items():
            new_dict[value] = key
    return new_dict

print(reserve_dict({"a": 1, "b": 2, "c": 3}))
