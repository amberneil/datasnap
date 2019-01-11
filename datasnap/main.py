from tqdm import tqdm
from humanfriendly import format_size
from .helpers import (build_sets, get_stats, hash_paths, build_size_index,
                     select_duplicate_sizes, total_size, valid_root)


def datasnap(root_folder, get_hashes=False, all_hashes=True, hash_type='md5', progressbar=False):
    
    if not valid_root(root_folder):
        raise ValueError('Not a valid folder: {}'.format(root_folder))

    dir_map, file_map = build_sets(root_folder)
    if not get_hashes:
        return (dir_map, file_map)

    if all_hashes:
        select_hash_set = None
        total_bytes = total_size(file_map)
    else:
        size_table = build_size_index(file_map)
        select_hash_set = select_duplicate_sizes(size_table)
        total_bytes = total_size(select_hash_set)
    
    with tqdm(total=total_bytes, disable=(not progressbar)) as pbar:
        hash_paths(
            file_map, select_paths=select_hash_set,
            hash_type=hash_type, callback=pbar.update
        )

    return (dir_map, file_map)