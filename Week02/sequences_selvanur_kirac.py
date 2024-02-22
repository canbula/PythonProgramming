my_list = [1, 2, 2, 3, 3, 3]
my_tuple = (1, 2, 2, 3, 3, 3)
my_set = {1, 2, 3}
my_dict = {"Math": 90, "Biology": 80}


def remove_duplicates(liste: list) -> list:
    return list(set(liste))

def list_counts(liste: list) -> dict:
    return {i: liste.count(i) for i in liste}
  
def reverse_dict(dictionary: dict) -> dict:
    return {v: k for k, v in dictionary.items()}

