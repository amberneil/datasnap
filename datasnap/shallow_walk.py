import time
from pathlib import Path
from .buildresult import buildresult

# This shallow walk will just go through folders level by level.
# Breaks when the timer runs out. Good for getting an idea of progress.
def shallow_walk(root_folder, timeout=5):
    start = time.time()
    level_dirs = [Path(root_folder)]
    while (time.time() - start) < timeout:
        sublevel_dirs = []
        for folder in level_dirs:
            for child in folder.iterdir():
                if child.is_dir():
                    sublevel_dirs.append(child)
                    yield buildresult(child.parent.resolve(), child.name)
        if len(sublevel_dirs) == 0:
            break
        level_dirs = sublevel_dirs