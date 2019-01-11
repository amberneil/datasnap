import hashlib

def md5_hash(path, callback=None):
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
            if callback:
                    callback(len(chunk))
                    
    return hash_md5.hexdigest()