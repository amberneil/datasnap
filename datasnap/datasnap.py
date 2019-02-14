import logging
import os
from .folderwalk import folderwalk
from .hashfuncs import md5_hash
from .helpers import get_stats
from .progress import _walk_progress_generator, _hash_progress_generator

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def datasnap(root_folder, hash=False, scan_timeout=5):
    
    if not os.path.isdir(root_folder):
        logger.error("Invalid folder passed as root.", extra={'folder': root_folder})
        raise ValueError('Not a valid folder: {}'.format(root_folder))
        
    folder_scan = folderwalk(root_folder, scan_timeout)
    walk_callback = _walk_progress_generator(folder_scan)
    
    buffer = []
    for path, dirs, files in os.walk(root_folder):
        for dr in dirs:
            directory_path = os.path.join(path, dr)
            walk_callback(directory_path)
            buffer.append((directory_path, get_stats(directory_path), True))
                
        for fi in files:
            file_path = os.path.join(path, fi)
            buffer.append((file_path, get_stats(file_path), False))

    if hash:
        hash_callback = _hash_progress_generator(buffer)
    for path, stats, isdir in buffer:
        if hash:
            if not isdir:
                stats['md5'] = md5_hash(path, callback=hash_callback)
        yield (path, stats, isdir)