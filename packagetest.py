from datasnap import datasnap
import time
from tqdm import tqdm
import logging
root = "/Volumes/AMBER_186F4"
root = "/Users/amberserver/Downloads"


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

class HashHandler(logging.Handler):
    pbar = None

    def progress(self, total):
        processed = 0
        with tqdm(total=total, bar_format=None) as pbar:
            while processed < total:
                new_bytes = (yield)
                processed += new_bytes
                pbar.update(new_bytes)

    def emit(self, record):
        if record.getMessage() == 'Hash total':
            print("Starting Hashes...")
            self.pbar = self.progress(record.total)
            self.pbar.send(None)
        if record.getMessage() == 'Hash progress':
            self.pbar.send(record.update)
            

logging.basicConfig(
    level=logging.INFO,
    handlers=[TqdmHandler(), HashHandler()]
)


files, dirs = datasnap(root, get_hashes=True)