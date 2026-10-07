def remove_duplicates(a_list):
    my_list = a_list[:]
    x = 1
    for i in my_list:
        for j in my_list[x:]:
            if i == j:
                my_list.remove(i)
                x -=1
                break
        x +=1
    
    return my_list
def list_counts(a_list):
    my_list = a_list[:]
    a = remove_duplicates(my_list)
    my_dict = dict.fromkeys(a)
    for i in a:
        x = 0
        for j in a_list:
            if i == j:
                x += 1
        my_dict[i] = x
            
    return my_dict
def reverse_dict(a_dict):
    my_dict = {}
    a_list = list(a_dict)
    b_list = list(a_dict.values())
    x = 0
    while x < len(a_list):
        print(1)
        my_dict[b_list[x]] = a_list[x]
        x += 1
            
    return my_dict

if __name__ == "__main__":
    print(remove_duplicates([1,5,4,4,4,6,41,54,54,41,6]))
    print(list_counts([1,5,5,4,4,4,6,6,6,41,41,41,41,41,54,54,54,54,54,54,54,54,41,6]))
    print(reverse_dict(list_counts([1,5,5,4,4,4,6,6,6,41,41,41,41,41,54,54,54,54,54,54,54,54,41,6])))