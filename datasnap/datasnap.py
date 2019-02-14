import logging
import os
from .folderwalk import folderwalk
from .helpers import get_stats
from .progress import _walk_progress_generator, _hash_progress_generator
from .hash import md5

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def _sort_by_level(buffer_item):
    name, stats, isdir = buffer_item
    path_parts = stats['parent'].split(os.sep)
    return (not isdir, len(path_parts))

def datasnap(root_folder, hash=False, scan_timeout=5):
    
    if not os.path.isdir(root_folder):
        logger.error("Invalid folder passed as root.", extra={'folder': root_folder})
        raise ValueError('Not a valid folder: {}'.format(root_folder))
        
    folder_scan = folderwalk(root_folder, scan_timeout)
    walk_callback = _walk_progress_generator(folder_scan)
    
    buffer = []
    for path, dirs, files in os.walk(root_folder):
        for directory_name in dirs:
            full_path = os.path.join(path, directory_name)
            walk_callback(full_path)
            buffer.append((directory_name, get_stats(full_path), True))
                
        for file_name in files:
            full_path = os.path.join(path, file_name)
            buffer.append((full_path, get_stats(full_path), False))

    if hash:
        hash_callback = _hash_progress_generator(buffer)
    for name, stats, isdir in sorted(buffer, key=_sort_by_level):
        if hash:
            if not isdir:
                full_path = os.path.join(stats['parent'], name)
                stats['md5'] = md5(full_path, callback=hash_callback)
        yield (name, stats, isdir)