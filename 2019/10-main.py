#!/usr/bin/env python3
import math
from collections import deque
data = None

with open('./10-data.txt') as f:
    data = f.read().splitlines()

w = len(data[0])
h = len(data)
p = []
c = []

for y in range(h):
    for x in range(w):
        if data[y][x] != '.':
            p.append((x,y))

def part1(p):
    for x0,y0 in p:
        slopes = {}
        for x1,y1 in p:
            if x1 == x0 and y1 == y0:
                continue
            dx = x1 - x0
            dy = y1 - y0
            nx = 0
            ny = 0
            m = 0
            if dy != 0:
                ny = dy/abs(dy)
            if dx == 0:
                m = (dy/abs(dy)) * math.inf
            else:
                nx = dx/abs(dx)
                m = (dy*1.0) / (dx*1.0)
            id = f'{m}_{nx}_{ny}'
            if slopes.get(id, None) is None:
                slopes[id] = 1
            #     if x0 == 5 and y0 == 8:
            #         print(f'add: {m} - {len(slopes)}')
            # else:
            #     if x0 == 5 and y0 == 8:
            #         print(f'dup: {m}')
        count = len(slopes)
        # print(f'{x0},{y0} = {count}')
        c.append(count)

    best = max(c)
    i = c.index(best)
    print(f'point: {p[i][0]}, {p[i][1]} - count: {best}')

part1(p[:])
  
def cross_zval(v):
    a = [0,-1]
    return a[0]*v[1] - a[1]*v[0]

def mag(v):
    return math.sqrt(v[0]**2 + v[1]**2)

def angle(v):
    dx,dy = v
    d = math.degrees(math.atan2(dx,-dy))
    if d < 0:
        d += 360
    return d

def part2(p):
    
    angles = {}
    o = (22, 28)
    x0,y0 = o
    for x1,y1 in p:
        if x1 == x0 and y1 == y0:
            continue
        dx = x1 - x0
        dy = y1 - y0
        
        m = mag([dx,dy])
        deg = angle([dx,dy])
        a = angles.get(deg, {})
        a[m] = (x1,y1)
        angles[deg] = a
        
    i = 0
    keylist = list(angles.keys())
    keylist.sort()
    # print(keylist)
    angle_keys = deque(keylist)
    zapped = []
    while len(angle_keys) > 0:
        if len(zapped) in [200]:
            print(f'{len(zapped)} zapped {zapped[-1]} - val: {zapped[-1][0]*100 + zapped[-1][1]}')
            if len(zapped) == 200:
                break
        k = angle_keys[0]
        pts = angles.get(k, None)
        if pts is not None and len(pts) > 0:
            pkeys = list(pts.keys())
            pkeys.sort()
            pi = pkeys.pop(0)
            p = pts[pi]
            zapped.append(p)
            # if len(zapped) in [1,2,3,10,11,12,13,14,20,50,100,199,200]:
            #     print(angle_keys[i])
            #     print(pts)
            del pts[pi]
        
        angle_keys.rotate(-1)

part2(p[:])



