import time
import os
from pathlib import Path 
from .hash import md5
from .buildresult import buildresult

def deep_walk(root_folder, hash=None, callback=None):
    for path, dirs, files in os.walk(root_folder):
        for d in dirs:
            yield buildresult(path, d)

            if callback:
                callback(1)

        for f in files:
            result = buildresult(path, f)
            if hash:
                result.stats['md5'] = md5(Path(path).joinpath(f).resolve())
            yield result

            if callback:
                callback(1)