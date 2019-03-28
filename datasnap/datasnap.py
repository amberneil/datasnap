from pathlib import Path
from .deep_walk import deep_walk
from .shallow_walk import shallow_walk

# Doesn't get much simpler than this.
def datasnap(root_folder, hash=False, shallow=False, callback=None):
    if not Path(root_folder).is_dir():
        raise NotADirectoryError(f'Not a directory: {root_folder}')
    
    if shallow:
        return shallow_walk(root_folder)
    
    return deep_walk(root_folder, hash=hash, callback=callback) 