#!/usr/bin/env python3

import re

data = None
with open('./12-data.txt') as f:
    data = f.read()

# data = r'[1,"red",{"a":[1,2,3],"b":{"n":"red","y":10}},{"red":false,"a":21},17]'
def print_sum(str):
    m = re.findall(r'-?\d+', str)
    s = sum([int(x) for x in m])
    print(s)

def strip_red_objs(data):
    red = ':"red"'

    while True:
        try:
            i = data.index(red)
        except:
            return data

        si = i
        ei = i + len(red)-1
        b = 1
        while b > 0:
            si -= 1
            c = data[si]
            
            if c == '}':
                b += 1
            elif c == '{':
                b -= 1

        c = data[ei]
        b = 1
        while b > 0:
            ei += 1
            c = data[ei]
            if c == '{':
                b += 1
            elif c == '}':
                b -= 1

        data = data[:si] +'{}'+ data[ei+1:]
    
# part 1
print('part 1:')
print_sum(data)

# part 2
print('part 2:')
data = strip_red_objs(data)
print_sum(data)