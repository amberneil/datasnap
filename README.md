# datasnap
Quickly snapshot a directory to extract stat metadata, checksums, and folder structure.

Mainly just uses os.stat, but adds in fields 'realpath', which follows symlinks, and 'exists' to identify whether Python feels the file exists.

'Exists' is useful to avoid FileNotFoundErrors if any operations will be done on files, and also can be helpful in identifying Mac aliases, where os.path.exists() => False.


```
>>> from datasnap import datasnap
>>> from pprint import pprint

>>> root = '/Users/amberneil/Desktop/B001'

>>> for name, parent, stats in datasnap(root):
>>>     print((name, parent))

('.DS_Store', '/Users/amberneil/Desktop/B001')

>>>     pprint(stats)

{       
        'islink': False,
        'isdir': False,
        'exists': True,
        'realpath': '/Users/amberneil/Desktop/B001/.DS_Store',
        'n_fields': 22,
        'n_sequence_fields': 10,
        'n_unnamed_fields': 3,
        'st_atime': 1548117757.2255864,
        'st_atime_ns': 1548117757225586315,
        'st_birthtime': 1355677440.0,
        'st_blksize': 4194304,
        'st_blocks': 24,
        'st_ctime': 1539575919.9607942,
        'st_ctime_ns': 1539575919960794171,
        'st_dev': 16777220, 
        'st_flags': 0,
        'st_gen': 0,
        'st_gid': 20,
        'st_ino': 2556233,
        'st_mode': 33279,
        'st_mtime': 1539575919.9607942,
        'st_mtime_ns': 1539575919960794171,
        'st_nlink': 1,
        'st_rdev': 0,
        'st_size': 6148,
        'st_uid': 50
    }

```
