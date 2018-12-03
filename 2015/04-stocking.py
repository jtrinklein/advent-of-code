#!/usr/bin/env python3
import hashlib

def hash(i):
    msg = f'bgvyzdsv{i}'.encode('utf-8')
    return hashlib.md5(msg).hexdigest()

def find_with_prefix(prefix, start=1, end=150000000):
    for i in range(start, end):
        h = hash(i)
        if h.startswith(prefix):
            print(f'first hash with prefix "{prefix}" is: {i} ({h})')
            return i

find_with_prefix('00000') #-> 254575
find_with_prefix('000000', start=254575)
