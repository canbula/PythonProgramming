my_list = ["ocean", "sea", "river"]

my_tuple = (1, 2, 3, 'a', 'b', 'c')

my_set = {"Martin Eden" , "Raskolnikov", "Simonov"}

my_dict = {
    "Los Angeles": "Lakers",
    "San Antonio": "Spurs",
    "Boston": "Celtics"
}


def remove_duplicates(my_list):
    updated_list =list(set(my_list))
    return updated_list



def list_counts(my_list):
    new_dict = {}
    for element in my_list:
        if element in new_dict:
            new_dict[element] += 1
        else:
            new_dict[element] = 1
    return new_dict            


def reverse_dict(my_dict):
    reversed_dict = {}
    for key, value in my_dict.items():
        reversed_dict[value] = key
    return reversed_dict    

