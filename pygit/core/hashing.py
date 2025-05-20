import hashlib

def hash_file(path):
    hash_object = hashlib.sha1()
    with path.open("rb") as f:
        while chunk := f.read(4096):
            hash_object.update(chunk)
    return hash_object.hexdigest()
