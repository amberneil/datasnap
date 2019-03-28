import os
from collections import namedtuple

# This is the eventual returned item from the walk. Thanks Raymond.
DataSnapItem = namedtuple('DataSnapItem', 'name parent stats')


# Stats should be a dict of os.stat, with 4 additions from Python.
def getstats(parent_path, name):
    file_path = os.path.join(parent_path, name)
    result = {}
    result['exists'] = os.path.exists(file_path)
    result['realpath'] = os.path.realpath(file_path)
    result['isdir'] = os.path.isdir(file_path)
    result['islink'] = os.path.islink(file_path)

    # Doing the below stuff, because dir(stat_result) has more metadata.
    try:
        stat_result = os.stat(file_path)
        for att in dir(stat_result):
            att_value = getattr(stat_result, att)
            if not callable(att_value) and att != '__doc__':
                result[att] = att_value

    # Alias files and the like will error on os.stat.
    except EnvironmentError as e:
        if e.strerror == 'No such file or directory':
            pass
        else:
            raise
    
    return result

def buildresult(parent_path, name):
    stats = getstats(parent_path, name)
    return DataSnapItem(name=name, parent=str(parent_path), stats=stats) 
