#!/usr/bin/env python3

data = None

with open('./10-data.txt') as f:
    data = f.read().splitlines()

points = []
for line in data:
    # print(line)
    pos, vel= line.split('> ')
    p = 'position=<'
    pos = [int(x) for x in pos[len(p):].split(', ')]
    v = 'velocity=<'
    vel = [int(x) for x in vel[len(v):-1].split(', ')]
    points.append(pos + vel)
    # print(pos,vel)

steps = 0

dx = 10000000000000000
dy = 10000000000000000
def step_back(points):
    global steps
    steps -= 1
    ret = []
    for p in points:
        p[0] -= p[2]
        p[1] -= p[3]
        ret.append(p)
    return ret
def step_points(points):
    global steps
    global dx
    global dy
    steps += 1
    ret = []
    for p in points:
        p[0] += p[2]
        p[1] += p[3]
        ret.append(p)

    xs = [x[0] for x in points]
    ys = [x[1] for x in points]
    maxx = max(xs)
    minx = min(xs)
    maxy = max(ys)
    miny = min(ys)
    cx = maxx - minx
    cy = maxy - miny
    if cx > dx or cy > dy:
        ret = step_back(ret)
        print(steps, ': smallest DX:', dx, '|', minx, miny, ',', maxx, maxy)
        print(steps, ': smallest DY:', dy, '|', minx, miny, ',', maxx, maxy)
        print_points(ret, minx, miny, maxx, maxy)
        return None
    else:
        dx = cx
        dy = cy
    return ret

def print_points(points, startx, starty, endx, endy):
    grid = []
    w = endx - startx
    h = endy - starty
    
    for y in range(h):
        grid.append([' ' for x in range(w)])

    for p in points:
        x,y,dx,dy = p
        x = x - startx
        y = y - starty
        if x < w and y < h:
            grid[y][x] = '#'
    
    print('________________________________________________________________________')
    for y in range(h):
        o = ''.join(grid[y])
        print(o)
    print('________________________________________________________________________')
        
working = True

while points is not None:
    points = step_points(points)

# while input('?') != 'x':
#     print_points(points, 190, 145 , 270, 170)
#     points = step_points(points)
