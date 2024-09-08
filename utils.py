import os

def load_dictionary(dict_path, delimiter=' '):
    dictionary = {}
    with open(dict_path) as f:
        for line in f:
            # print('line: {}'.format(line))
            k, v = line.strip().split(delimiter, 1)
            dictionary[k.lower()] = v 
    
    return dictionary