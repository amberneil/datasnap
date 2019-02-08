from datasnap import datasnap
from datasnap.progress import WalkProgress
import time
from tqdm import tqdm
import logging
root = "/Volumes/AMBER_186F4"


class TqdmHandler(logging.Handler):
    pbar = None

    def progress(self, total):
        with tqdm(total=total, bar_format=None) as pbar:
            for i in range(total):
                pbar.update((yield))
        yield
        
    def emit(self, record):
        if record.getMessage() == 'Shallow total':
            self.pbar = self.progress(record.total)
            self.pbar.send(None)
        if record.getMessage() == 'Shallow progress':
            self.pbar.send(record.update)
            

logging.basicConfig(
    level=logging.INFO,
    handlers=[TqdmHandler()]
)


files, dirs = datasnap(root)