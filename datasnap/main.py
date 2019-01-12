print(__name__)


from .helpers.progress import WalkProgress, HashProgress
from .helpers.helpers import (build_sets,  hash_paths, build_size_index,
                     select_duplicate_sizes, total_size, valid_root)


def datasnap(root_folder, get_hashes=False, all_hashes=True, hash_type='md5', progressbar=False):
    
    if not valid_root(root_folder):
        raise ValueError('Not a valid folder: {}'.format(root_folder))
    
    with WalkProgress(root_folder, disable=(not progressbar)) as pbar:
        dir_map, file_map = build_sets(root_folder, callback=pbar.update)

    if get_hashes:
    
        with HashProgress(
            file_map, all_hashes=all_hashes, disable=(not progressbar)
            ) as pbar:

            hash_paths(
                file_map, select_paths=pbar.select_hash_set,
                hash_type=hash_type, callback=pbar.update
            )

    return (dir_map, file_map)