my_list = [ "Berlin", "Paris", "Roma", "İstanbul", "Prag","Madrid"]
my_tuple = (1, 2, 3, 5, 8, 13)
my_set = {19, 18, 17, 16, 15, 14}
my_dict = {"Paris": "Fransa",
            "Roma": "İtalya",
            "İstanbul":"Türkiye",
            "Prag": "Çekya",
            "Madrid": "İspanya"
            "Berlin": "Almanya"}


def remove_duplicates(my_list):
    return list(set(my_list))


def list_counts(my_list):
  counts = {}
  for item in my_list:
      if item in counts:
          counts[item] += 1
      else:
          counts[item] = 1
  return counts


  def reverse_dict (my_dict):
    return  {value: key for key, value in my_dict.items()}
