# datasnap
Quickly snapshot a directory to extract stat metadata, checksums, and folder structure.

Mainly just uses os.stat, but adds in fields 'realpath', which follows symlinks, and 'exists' to identify whether Python feels the file exists.

'Exists' is useful to avoid FileNotFoundErrors if any operations will be done on files, and also can be helpful in identifying Mac aliases, where os.path.exists() => False.


```
>>> from datasnap import datasnap

>>> root = '/Users/amberneil/Desktop/B001'

>>> dirs, files = datasnap(root)

>>> dirs
{
    '/Users/amberneil/Desktop/B001/MISC': {
        'exists': True,
        'realpath': '/Users/amberneil/Desktop/B001/MISC',
        'parent': '/Users/amberneil/Desktop/B001',
        'n_fields': 22,
        'n_sequence_fields': 10,
        'n_unnamed_fields': 3,
        'st_atime': 1548117757.2528446,
        'st_atime_ns': 1548117757252844520,
        'st_birthtime': 1537378808.0,
        'st_blksize': 4194304,
        'st_blocks': 0,
        'st_ctime': 1538166838.6238775,
        'st_ctime_ns': 1538166838623877549,
        'st_dev': 16777220,
        'st_flags': 0,
        'st_gen': 0,
        'st_gid': 20,
        'st_ino': 2556235,
        'st_mode': 16895,
        'st_mtime': 1537378808.0,
        'st_mtime_ns': 1537378808000000000,
        'st_nlink': 2,
        'st_rdev': 0,
        'st_size': 64,
        'st_uid': 501
    },
    '/Users/amberneil/Desktop/B001/DCIM': { ... },
    '/Users/amberneil/Desktop/B001/DCIM/100EOS7D': { ... }
}

>>> files
{
    '/Users/amberneil/Desktop/B001/.DS_Store': {
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
    '/Users/amberneil/Desktop/B001/DCIM/.DS_Store': { ... },
    '/Users/amberneil/Desktop/B001/DCIM/100EOS7D/MVI_1083.MOV': { ... },
    '/Users/amberneil/Desktop/B001/DCIM/100EOS7D/MVI_1084.MOV': { ... },
    '/Users/amberneil/Desktop/B001/DCIM/100EOS7D/MVI_1086.MOV': { ... },
    '/Users/amberneil/Desktop/B001/DCIM/100EOS7D/_MG_1079.JPG': { ... },
    '/Users/amberneil/Desktop/B001/DCIM/100EOS7D/_MG_1078.JPG': { ... },
    '/Users/amberneil/Desktop/B001/DCIM/100EOS7D/MVI_1077.THM': { ... },
    '/Users/amberneil/Desktop/B001/DCIM/100EOS7D/_MG_1078.CR2': { ... },
    '/Users/amberneil/Desktop/B001/DCIM/100EOS7D/_MG_1079.CR2': { ... },
    '/Users/amberneil/Desktop/B001/DCIM/100EOS7D/MVI_1083.THM': { ... },
    '/Users/amberneil/Desktop/B001/DCIM/100EOS7D/MVI_1082.THM': { ... }   

}

```
