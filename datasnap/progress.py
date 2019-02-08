import logging
from tqdm import tqdm
from .folderwalk import folderwalk
from .helpers import total_size, build_size_index, select_duplicate_sizes

logger = logging.getLogger(__name__)

class WalkProgress():
    def __init__(self, root_folder, timeout=5, callback=None, show=False):
        self.timeout = timeout
        self.callback = callback
        logger.info('Starting shallow walk')
        self.folders = folderwalk(root_folder, self.timeout)
        logger.info('Finished shallow walk')
        self.total = len(self.folders)
        logger.info('Shallow total', extra={'total': self.total})
        self.pbar = tqdm(total=self.total, disable=(not show))
    
    def update(self, processed_dir):
        if processed_dir in self.folders:
            if self.callback:
                self.callback(1)
            self.pbar.update(1)
            logger.info('Shallow progress', extra={'update': 1})
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.pbar.close()

class HashProgress():
    def __init__(self, file_map, all_hashes=True, disable=False):
        if all_hashes:
            self.select_hash_set = None
            self.total_bytes = total_size(file_map)
            logger.info('Hash total', extra={'total': self.total_bytes})
        else:
            size_table = build_size_index(file_map)
            self.select_hash_set = select_duplicate_sizes(size_table)
            self.total_bytes = total_size(
                file_map, select_paths=self.select_hash_set
            )

        self.pbar = tqdm(total=self.total_bytes, disable=disable)
    
    def update(self, num):
        self.pbar.update(num)
        logger.info('Hash progress', extra={'update': num})
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.pbar.close()
