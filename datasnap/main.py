from tqdm import tqdm
from humanfriendly import format_size
from .helpers import build_sets, get_stats, hash_paths, build_size_index, select_duplicate_sizes


def datasnap(root_folder, get_hashes=False, all_hashes=False, hash_type='md5', progressbar=False):
    dir_map, file_map = build_sets(root_folder)

    if not get_hashes:
        return (dir_map, file_map)
    if all_hashes:
        select_hash_set = None
    else:
        size_table = build_size_index(file_map)
        select_hash_set = select_duplicate_sizes(size_table)

    total_to_hash = len(select_hash_set) if select_hash_set else len(file_map.keys())
    with tqdm(total=total_to_hash, disable=(not progressbar)) as pbar:
        hash_paths(
            file_map, select_paths=select_hash_set,
            hash_type=hash_type, callback=pbar.update
        )

    return (dir_map, file_map)