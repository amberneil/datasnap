import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def _gen_wrap(gen_func):
    def gen_wrapper(startvalue):
        generator = gen_func(startvalue)
        generator.send(None)
        return generator.send
    return gen_wrapper

@_gen_wrap
def _walk_progress_generator(folder_scan):
    total = len(folder_scan)
    logger.info('Shallow total', extra={'total': total})
    while True:
        path = (yield)
        if path in folder_scan:
            logger.info('Shallow progress', extra={'update': 1, 'total': total})
@_gen_wrap
def _hash_progress_generator(buffer):
    total = 0
    for path, stats, isdir in buffer: 
        if not isdir:
            total += stats.get('st_size', 0)
    logger.info('Hash total', extra={'total': total})
    while True:
        processed_bytes = (yield)
        logger.info('Hash progress', extra={'update': processed_bytes, 'total': total})
