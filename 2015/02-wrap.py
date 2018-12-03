#!/usr/local/bin/python3

data = None
with open('./02-data.txt') as f:
    data = f.read()

items = data.split('\n')
print(f"item count: {len(items)}")
a = 0
r = 0
#items = ['2x3x4', '1x1x10']
for i in items:
    w,h,l = [int(x) for x in i.split('x')]

    dims = [w,h,l]
    dims.sort()
    areas = [w*h, h*l, l*w]
    vol = w*h*l
    first = dims[:2]
    last = dims[1:]

    r += (min(first) * 2) + (min(last)*2) + vol

    a += sum(areas*2) + min(areas)
    
print(f"required paper: {a}")
print(f'required ribbon: {r}')