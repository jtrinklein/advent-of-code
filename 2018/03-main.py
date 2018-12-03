#!/usr/local/bin/python3

data = None

with open('./03-data.txt') as f:
    data = f.read().splitlines()
a = 0
v = []
for x in range(1000):  
    for y in range(1000):
        v.append(0)

# part 1
coords = []
for line in data:
    id,c = line.split(' @ ')
    start,end = c.split(': ')
    x,y = [int(x) for x in start.split(',')]
    w,h = [int(x) for x in end.split('x')]
    for xx in range(x, x+w):
        for yy in range(y, y+h):
            v[xx + yy*1000] += 1
    coords.append((id, x,y,w,h))
c = len([x for x in v if x > 1])

print(c)


# part 2
for set1 in coords:
    
    id1,x1,y1,w1,h1 = set1
    collision = False
    for set2 in coords:
        id2,x2,y2,w2,h2 = set2
        if id1 == id2 or collision:
            continue

        if x1 < x2 + w2 and \
            x1 + w1 > x2 and \
            y1 < y2 + h2 and \
            y1 + h1 > y2:
                collision = True

    
    if not collision:
        print('did not collide:', id1)
        break
