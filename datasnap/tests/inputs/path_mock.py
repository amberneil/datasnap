from collections import namedtuple
import os

MockPath = namedtuple('MockPath', 'path isdir')
mock_data = [
    MockPath('test', True),
    MockPath('test/doc.txt', False),
    MockPath('test/nofaile.txt', False),
    MockPath('test/deeptest', True),
    MockPath('test/deeptest2', True),
    MockPath('test/deeptest3', True),
    MockPath('test/notatest.txt', False),
    MockPath('test/notatest2.txt', False),
    MockPath('test/nojoke.txt', False),
    MockPath('test/deeptest/ifollow', True),
    MockPath('test/deeptest/ifollow/youdeepseababy', True),
    MockPath('test/deeptest/ifollow/youdeepseababy/lyrics.txt', False),
    MockPath('test/deeptest2/howdeepdoesthisgo', True),
    MockPath('test/deeptest2/howdeepdoesthisgo/justtohere.txt', False),
    MockPath('test/deeptest3/howdeepisyourlove', True),
    MockPath('test/deeptest3/howdeepisyourlove/lyrics.txt', False),
]

def mock_path_structure(tmp_path):
    prefix = '/Users/amberserver/Desktop/'
    for item in mock_data:
        path = tmp_path / item.path
        if not path.exists():
            if item.isdir:
                path.mkdir()
            else:
                path.touch()
