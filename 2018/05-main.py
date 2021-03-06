#!/usr/bin/env python3
import re

data = None
with open('./05-data.txt') as f:
    data = f.read()
# data = 'dabAcCaCBAcCcaDA'

lowers = 'abcdefghijklmnopqrstuvwxyz'
uppers = lowers.upper()

def react_polimer(data):
    reacted = True
    reactioncount = 0
    while reacted:
        reactioncount += 1
        reacted = False
        next = ''
        count = len(data)
        i = 0
        while i < count:
            x = data[i]
            i += 1
            
            if i == count:
                next += x
                continue

            y = data[i]

            if (x in lowers and x.upper() == y ) or  (x in uppers and x.lower() == y):
                reacted = True
                i += 1
            else:
                next += x

        data = next
    return data

def part_1(data):
    reacted = react_polimer(data)
    print('length:', len(reacted), len(reacted) == 11264)

def part_2(data):

    minlength = 1000000
    for i in lowers:
        stripped = re.sub(i, '', data, flags=re.IGNORECASE)
        reacted = react_polimer(stripped)
        l = len(reacted)
        print(i, l)
        if l < minlength:
            minlength = l
    print('min:', minlength)

# part_1(data)
part_2(data)