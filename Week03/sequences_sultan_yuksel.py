def remove_duplicates(seq: list) -> list:
  new_list = []
  for i in seq:
    if i not in new_list:
      new_list.append(i)
  return new_list

def list_counts(seq: list) -> dict:
  counts = {}
  for i  in seq:
    if i in counts:
      counts[i] += 1
    else:
      counts[i]
  return counts

def reverse_dict(d: dict) ->dict:
  new_dict = {}
  for key, value in d.items():
    new_dict[value] = key
  return new_dict
