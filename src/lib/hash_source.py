import hashlib

def hash(source):

    return hashlib.sha512(source.encode('utf-8')).hexdigest()
