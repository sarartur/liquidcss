import os
from hashlib import sha256


def create_file_key(path):
    components = path.split(os.sep)
    return "~".join(components)

def create_file_hash(path):
    with open(path, 'r') as file:
        return sha256(file.read().encode('utf-8')).hexdigest()