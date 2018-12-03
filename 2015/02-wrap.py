#!/usr/bin/env python3

data = None
with open('./02-data.txt') as f:
    data = f.read()

items = data.split('\n')

paper = 0
ribbon = 0

for i in items:
    w,h,l = [int(x) for x in i.split('x')]

    dims = [w,h,l]
    dims.sort()
    areas = [w*h, h*l, l*w]
    vol = w*h*l
    first = dims[:2]
    last = dims[1:]

    ribbon += (min(first) * 2) + (min(last)*2) + vol

    paper += sum(areas*2) + min(areas)
    
print(f"required paper: {paper}")
print(f'required ribbon: {ribbon}')