from datasnap import datasnap
import os
import shelve
from pprint import pprint
import time
from tqdm import tqdm
import logging

root = "/Users/amberserver/Downloads"

class LogProgress(logging.Handler):
    def __init__(self):
        self.pbar = None
        super(LogProgress, self).__init__()

    def _prog_gen(self, total):
        count = 0
        with tqdm(total=total, bar_format=None) as pbar:
            while count < total:
                value = yield
                count += value
                pbar.update(value)
        yield
    
    def emit(self, record):
        if record.getMessage() == self._total_log:
            print("\n" + self.message)
            self.pbar = self._prog_gen(record.total)
            self.pbar.send(None)
        if record.getMessage() ==  self._update_log:
            self.pbar.send(record.update)

class WalkLog(LogProgress):
        _total_log = 'Shallow total'
        _update_log = 'Shallow progress'
        message = "Walking root directory..."

class HashLog(LogProgress):
        _total_log = 'Hash total'
        _update_log = 'Hash progress'
        message = "Hashing root directory..."

            

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(WalkLog())
logger.addHandler(HashLog())


# with shelve.open('packagecache') as db:
#     db['data'] = [i for i in datasnap(root, hash=False)]
count = 0
for name, stats, isdir in datasnap(root, hash=False):
    count += 1
    if count > 100:
        break
    print(os.path.join(stats['parent'], name), isdir)