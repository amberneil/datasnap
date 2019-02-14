import os
from .hashfuncs import md5_hash
import errno

def get_stats(file_path):
    result = {}
    result['exists'] = os.path.exists(file_path)
    result['realpath'] = os.path.realpath(file_path)
    result['parent'] = os.path.abspath(os.path.join(file_path, os.pardir))
    try:
        stat_result = os.stat(file_path)
        for att in dir(stat_result):
            att_value = getattr(stat_result, att)
            if not callable(att_value) and att != '__doc__':
                result[att] = att_value
    except EnvironmentError as e:
        if os.strerror(e.errno) == 'No such file or directory':
            pass
    
    return result