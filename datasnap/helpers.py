import os

def get_stats(file_path):
    result = {}
    stat_result = os.stat(file_path)
    for att in dir(stat_result):
        att_value = getattr(stat_result, att)
        if not callable(att_value) and att != '__doc__':
            result[att] = att_value
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