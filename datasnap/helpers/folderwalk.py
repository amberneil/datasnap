import os
import time

def list_child_dirs(path):
    result = set()
    for f in os.listdir(path):
        fullpath = os.path.join(path, f)
        if os.path.isdir(fullpath):
            if os.path.realpath(fullpath) == fullpath:
                result.add(fullpath)
    return result

def folderwalk(root, timeout=None):
    key_dirs = set()
    assert os.path.exists(root)
    if timeout is not None:
        condition = lambda now, timeout: now < timeout
    else:
        condition = lambda x, y: True

    start = time.time()
    while condition(time.time() - start, timeout):
        if len(key_dirs) == 0:
            upper_level_dirs = list_child_dirs(root)
            key_dirs = set(list_child_dirs(root))

        this_level_dirs = set()
        for dr in upper_level_dirs:
            child_dirs = list_child_dirs(dr)
            this_level_dirs.update(child_dirs)
            key_dirs.update(child_dirs)
            upper_level_dirs = this_level_dirs

        if not this_level_dirs:
            break
    return key_dirs