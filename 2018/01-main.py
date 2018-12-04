#!/usr/bin/env python3

data = None

with open('./01-data.txt') as f:
    data = f.read().splitlines()

ss = {}
s = 0
ss[s] = True

def check(data):
    global ss
    global s
    for line in data:
        s += int(line)

        if ss.get(s, False):
            return s

        ss[s] = True
    return None


v = check(data)
print('after first pass:', s)
while v is None:
    v = check(data)
print('first duplicate:', v)