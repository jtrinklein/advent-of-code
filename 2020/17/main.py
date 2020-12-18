#!/usr/bin/env python3

data = []

with open('./data.txt') as f:
    data = [[1 if x == '#' else 0 for x in list(line.strip())] for line in f.readlines()]

'''
Sample 1
.#.
..#
###
'''
# data = [
#     [0,1,0],
#     [0,0,1],
#     [1,1,1],
# ]


def key_to_point(k):
    return [int(x) for x in k.split(',')]
def point_to_key(x,y,z):
    return f'{x},{y},{z}'
def get_state_at(x,y,z, grid):
    return grid.get(point_to_key(x,y,z), 0)

def set_state_at(x,y,z,value, grid):
    grid[point_to_key(x,y,z)] = value

def next_state(x,y,z,grid):
    '''
    If a cube is active 
      and exactly 2 or 3 of its 26 neighbors are also active,
            the cube remains active.
      Otherwise, the cube becomes inactive.
    If a cube is inactive 
        but exactly 3 of its 26 neighbors are active,
            the cube becomes active. 
        Otherwise, the cube remains inactive.
    '''
    total = sum(get_state_at(xi,yi,zi, grid) for zi in range(z-1, z+2) for yi in range(y-1, y+2) for xi in range(x-1, x+2))

    my_state = get_state_at(x,y,z,grid)

    # don't include my state when considering alive near me
    total -= my_state

    if my_state:
        if 2 <= total and total <= 3:
            return 1
        else:
            return 0
    elif total == 3:
        return 1
    return 0
    
def do_cycle(grid):
    result = {}
    to_check = []
    for k,v in grid.items():
        # check active spaces
        if v == 1:
            x,y,z = key_to_point(k)
            p = [x,y,z]
            if not p in to_check:
                to_check.append(p)
            # also check all 26 spaces touching this
            for zi in range(z-1, z+2):
                for yi in range(y-1, y+2):
                    for xi in range(x-1, x+2):
                        p = [xi,yi,zi]
                        if not p in to_check:
                            to_check.append(p)
    for x,y,z in to_check:
        state = next_state(x,y,z, grid)
        set_state_at(x,y,z, state, result)
    return result

def gridprint(grid):
    points = [key_to_point(k) for k,v in grid.items() if v == 1]
    minz = min(z for x,y,z in points) if len(points) > 0 else 0
    maxz = max(z for x,y,z in points) if len(points) > 0 else 0
    miny = min(y for x,y,z in points) if len(points) > 0 else 0
    maxy = max(y for x,y,z in points) if len(points) > 0 else 0
    minx = min(x for x,y,z in points) if len(points) > 0 else 0
    maxx = max(x for x,y,z in points) if len(points) > 0 else 0

    for z in range(minz,maxz+1):
        print(f'z: {z}')
        for y in range(miny, maxy+1):
            for x in range(minx, maxx+1):
                if [x,y,z] in points:
                    print('#', end='')
                else:
                    print('.', end='')
            print('')
        print('\n--------------')
    print('=================================')

def build_grid(d):
    grid = {}
    for y in range(len(d)):
        for x in range(len(d[0])):
            if d[y][x] == 1:
                set_state_at(x,y,0, 1, grid)
    return grid

def part1(d):
    grid = build_grid(d)
    for _ in range(6):
        grid = do_cycle(grid)
    c = sum(grid.values())
    print(f'{c} active cells')


part1(data)


