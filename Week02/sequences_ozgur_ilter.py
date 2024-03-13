my_list = [12 ,'ozgur', 75 , True]
my_tuple = (12,1.5, 'python')
my_set = {'python', 'java', 'javascript'} 
my_dict = {
    'name' : 'Ozgur',
    'surname': 'Ilter',
    'country' : 'Turkey'
}

def remove_duplication(a_list):
    return list(set(a_list))


def list_counts(a_list):
    return {i: a_list.count(i) for i in a_list}


def reverse_dict(my_dict):
     return {v: k for k, v in my_dict.items()}

