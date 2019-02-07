from tqdm import tqdm
from .folderwalk import folderwalk
from .helpers import total_size, build_size_index, select_duplicate_sizes

class WalkProgress():
    def __init__(self, root_folder, callback=None, show=False):
        self.timeout = 5
        self.callback = callback
        self.folders = folderwalk(root_folder, 5)
        self.total = len(self.folders)
        self.pbar = tqdm(total=self.total, disable=(not show))
    
    def update(self, processed_dir):
        if processed_dir in self.folders:
            if self.callback:
                self.callback(1)
            self.pbar.update(1)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.pbar.close()

class HashProgress():
    def __init__(self, file_map, all_hashes=True, disable=False):
        if all_hashes:
            self.select_hash_set = None
            self.total_bytes = total_size(file_map)
        else:
            size_table = build_size_index(file_map)
            self.select_hash_set = select_duplicate_sizes(size_table)
            self.total_bytes = total_size(
                file_map, select_paths=self.select_hash_set
            )

        self.pbar = tqdm(total=self.total_bytes, disable=disable)
    
    def update(self, num):
        self.pbar.update(num)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.pbar.close()
