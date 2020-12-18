#!/usr/bin/env python3

data = []

with open('./data.txt') as f:
    data = [[1 if x == '#' else 0 for x in list(line.strip())] for line in f.readlines()]

def key_to_point(k):
    return k

def point_to_key(x,y,z,w):
    return (x,y,z,w)

def get_state_at(grid, x,y,z,w):
    return grid.get(point_to_key(x,y,z,w), 0)

def set_state_at(grid, value, x,y,z,w):
    grid[point_to_key(x,y,z,w)] = value

def next_state(grid,x,y,z,w,use_4_dimensions=False):
    '''
    If a cube is active 
      and exactly 2 or 3 of its neighbors are also active,
            the cube remains active.
      Otherwise, the cube becomes inactive.
    If a cube is inactive 
        but exactly 3 of its neighbors are active,
            the cube becomes active. 
        Otherwise, the cube remains inactive.
    '''
    wrange = range(w-1,w+2) if use_4_dimensions else [w]
    total = sum(get_state_at(grid,xi,yi,zi,wi) for zi in range(z-1, z+2) for yi in range(y-1, y+2) for xi in range(x-1, x+2) for wi in wrange)

    my_state = get_state_at(grid,x,y,z,w)

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
    
def do_cycle(grid,use_4_dimensions=False):
    result = {}
    to_check = []

    for k,v in grid.items():
        # check active spaces
        if v == 1:
            p = key_to_point(k)
            x,y,z,w = p
            if not p in result:
                to_check.append(p)
            # also check all spaces touching this
            # 26 if in 3 dimensions
            # 80 if in 4 dimensions
            wrange = range(w-1,w+2) if use_4_dimensions else [w]
            for wi in wrange:
                for zi in range(z-1, z+2):
                    for yi in range(y-1, y+2):
                        for xi in range(x-1, x+2):
                            p = point_to_key(xi,yi,zi,wi)
                            if not p in result:
                                to_check.append(p)
    for x,y,z,w in to_check:
        state = next_state(grid, x,y,z,w, use_4_dimensions=use_4_dimensions)
        set_state_at(result, state, x,y,z,w)
    return result

def gridprint(grid):
    points = [key_to_point(k) for k,v in grid.items() if v == 1]
    minw = min(w for x,y,z,w in points)
    maxw = max(w for x,y,z,w in points)
    minz = min(z for x,y,z,w in points)
    maxz = max(z for x,y,z,w in points)
    miny = min(y for x,y,z,w in points)
    maxy = max(y for x,y,z,w in points)
    minx = min(x for x,y,z,w in points)
    maxx = max(x for x,y,z,w in points)

    for w in range(minw, maxw + 1):
        for z in range(minz,maxz+1):
            print(f'z: {z}, w: {w}')
            for y in range(miny, maxy+1):
                for x in range(minx, maxx+1):
                    k = point_to_key(x,y,z,w)
                    if k in points:
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
                set_state_at(grid, 1, x,y,0,0)
    return grid

def part1(d):
    grid = build_grid(d)
    # gridprint(grid)
    # grid = do_cycle(grid)
    # gridprint(grid)
    # grid = do_cycle(grid)
    # gridprint(grid)
    for _ in range(6):
        grid = do_cycle(grid)
    c = sum(grid.values())
    print(f'{c} active cells')

def part2(d):
    grid = build_grid(d)
    # gridprint(grid)
    # grid = do_cycle(grid, use_4_dimensions=True)
    # gridprint(grid)
    for _ in range(6):
        grid = do_cycle(grid, use_4_dimensions=True)
    
    c = sum(grid.values())
    print(f'{c} active cells')

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

part2(data)
