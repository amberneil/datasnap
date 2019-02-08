import logging
from .progress import WalkProgress, HashProgress
from .helpers import (build_sets,  hash_paths, build_size_index,
                     select_duplicate_sizes, total_size, valid_root)

logger = logging.getLogger(__name__)

def datasnap(root_folder, get_hashes=False, all_hashes=True, hash_type='md5', progresshandler=None, progressbar=False):
    
    if not valid_root(root_folder):
        raise ValueError('Not a valid folder: {}'.format(root_folder))
        logger.error("Invalid folder passed as root.", extra={'folder': root_folder})
    
    if not progresshandler:
        progresshandler = WalkProgress(root_folder, show=progressbar)
        logger.info("Using default progress handler", extra={'handler': repr(progresshandler)})
    else:
        logger.info("Using passed parameter as progress handler", extra={'handler': repr(progresshandler)})
    
      
    with progresshandler as pbar:
        dir_map, file_map = build_sets(root_folder, callback=pbar.update)

    if get_hashes:
        logger.info("Starting hash process", extra={'all_hashes': all_hashes}) 
        with HashProgress(
            file_map, all_hashes=all_hashes, disable=(not progressbar)
            ) as pbar:

            hash_paths(
                file_map, select_paths=pbar.select_hash_set,
                hash_type=hash_type, callback=pbar.update
            )

    return (dir_map, file_map)
