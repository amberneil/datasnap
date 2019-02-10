import logging

from .folderwalk import folderwalk
from .helpers import (build_sets, hash_paths, valid_root)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def _walk_progress_generator(folder_scan):
    total = len(folder_scan)
    logger.info('Shallow total', extra={'total': total})
    while True:
        path = (yield)
        if path in folder_scan:
            logger.info('Shallow progress', extra={'update': 1, 'total': total})

def _hash_progress_generator(file_map):
    total = sum(file_map[path].get('st_size', 0) for path in file_map.keys())
    logger.info('Hash total', extra={'total': total})
    while True:
        processed_bytes = (yield)
        logger.info('Hash progress', extra={'update': processed_bytes, 'total': total})



def datasnap(root_folder, get_hashes=False, scan_timeout=5):
    
    if not valid_root(root_folder):
        logger.error("Invalid folder passed as root.", extra={'folder': root_folder})
        raise ValueError('Not a valid folder: {}'.format(root_folder))
        
    # Logic to get a rough total of folders and send to logs
    logger.info('Starting folder scan')
    folder_scan = folderwalk(root_folder, scan_timeout)
    prog_gen = _walk_progress_generator(folder_scan)
    prog_gen.send(None)
    # Actual walk function.
    dir_map, file_map = build_sets(root_folder, callback=lambda x: prog_gen.send(x))
    

    if get_hashes:
        # Logic to log hash progress
        logger.info("Starting hash process")
        prog_gen = _hash_progress_generator(file_map)
        prog_gen.send(None)
        # Actual hash function
        hash_paths(file_map, callback=lambda x: prog_gen.send(x))

    return (dir_map, file_map)
