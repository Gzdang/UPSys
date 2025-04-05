import hashlib
import json

def load_json(path):
    with open(path, "r") as file:
        data = json.load(file)
    return data

def get_md5(content):
    md5hash = hashlib.md5(content.encode('utf-8'))
    return md5hash.hexdigest()