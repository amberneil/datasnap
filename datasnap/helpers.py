import os
from .hashfuncs import md5_hash

def get_stats(file_path):
    result = {}
    result['exists'] = os.path.exists(file_path)
    result['realpath'] = os.path.realpath(file_path)
    try:
        stat_result = os.stat(file_path)
        for att in dir(stat_result):
            att_value = getattr(stat_result, att)
            if not callable(att_value) and att != '__doc__':
                result[att] = att_value
    except FileNotFoundError:
        pass
    
    return result
        

def build_sets(root_folder):
    directory_set = {}
    file_set = {}
    for path, dirs, files in os.walk(root_folder):
        for dr in dirs:
            directory_path = os.path.join(path, dr)
            directory_set[directory_path] = get_stats(directory_path)
        for fi in files:
            file_path = os.path.join(path, fi)
            file_set[file_path] = get_stats(file_path)
    return (directory_set, file_set)

def build_size_index(file_map):
    table = {}
    for path, data in file_map.items():
        size = data.get('st_size', 0)
        if not table.get(size):
            table[size] = set()
        table[size].add(path)
    return table

def select_duplicate_sizes(size_index):
    return_set = set()
    for size in size_index.keys():
        if len(size_index[size]) > 1:
            for file_path in size_index[size]:
                return_set.add(file_path)
    return return_set


def hash_paths(file_map, select_paths=None, hash_type='md5', callback=None):
    func_map = { 'md5': md5_hash }
    hash_type = hash_type.lower()
    if not func_map.get(hash_type):
            raise ValueError(
                'Hash_type must be one of: {}.'.format(", ".join(func_map.keys()))
            )

    if select_paths:
        path_list = select_paths
    else:
        path_list = file_map.keys()
    
    for path in path_list:
        if not file_map.get(path):
            raise KeyError(
                'Get_hashes given path not in main file_dict: {}'.format(path)
            )
        if file_map[path]['exists']:
            file_map[path][hash_type] = func_map[hash_type](path)

        if callback:
            callback(1)