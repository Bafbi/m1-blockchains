def simple_hash(string):
    hash = 0
    for c in string:
        hash += ord(c)
        hash = hash ^ hash * 31
        hash = hash % 2**32
    return hash