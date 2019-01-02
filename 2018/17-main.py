#!/usr/bin/env python3

data = None

with open('./17-data.txt') as f:
    data = f.read().splitlines()
#.....+............
#......................
#......................
#...#............#....#
##..#...#...#....#....#
##..#...#...#....#....#
#...#...#####....#....#
#...#............#....#
#...##############....#
#.....................#
#.....................#
#.....................#
#.....................#
#.....................#
#.....................#

# data = [
#     'x=480, y=1..4',   # wall
#     'x=523, y=3..14',  # wall

#     # #big container
#     # 'x=495, y=2..12',
#     # 'y=12, x=495..515',
#     # 'x=515, y=3..12',

#     #big container lower
#     'x=490, y=13..22',
#     'y=22, x=490..515',
#     'x=515, y=13..22',

#     # #little box on edge
#     # 'x=495, y=4..8',
#     # 'x=500, y=5..8',
#     # 'y=8, x=495..500',


#     #little box
#     'x=498, y=5..7',
#     'x=502, y=5..7',
#     'y=7, x=498..502',
#     # 'y=5, x=498..502',
    
#     # #little box not in the way
#     # 'x=498, y=5..7',
#     # 'x=499, y=5..7',
# ]

#example:
#  ............#.
#  .#..#.......#.
#  .#..#..#......
#  .#..#..#......
#  .#.....#......
#  .#.....#......
#  .#######......
#  ..............
#  ..............
#  ....#.....#...
#  ....#.....#...
#  ....#.....#...
#  ....#######...
# data = [
#     'x=495, y=2..7',
#     'y=7, x=495..501',
#     'x=501, y=3..7',
#     'x=498, y=2..4',
#     'x=506, y=1..2',
#     'x=498, y=10..13',
#     'x=504, y=10..13',
#     'y=13, x=498..504',
# ]
grid = []
min_x = 1000
min_y = 1000
max_x = 0
max_y = 0

width = -1
height = -1

#chosen at random
SAND = 0
CLAY = 3
WATER = 1

def check_x(x):
    global min_x
    global max_x

    if x < min_x:
        min_x = x
    if x > max_x:
        max_x = x

def check_y(y):
    global min_y
    global max_y

    if y < min_y:
        min_y = y
    if y > max_y:
        max_y = y

def get_min_max(data):
    global width
    global height
    global min_x
    global max_x

    for line in data:
        #x=480, y=133..143
        const, var = line.split(', ')
        start,end = [int(x) for x in var.split('=')[-1].split('..')]
        
        isVertical = const.startswith('x=')
        if isVertical:
            x = int(const.split('=')[-1])
            y = start
            check_y(end)
        else:
            y = int(const.split('=')[-1])
            x = start
            check_x(end)

        check_x(x)
        check_y(y)
    min_x -= 10
    max_x += 10
    width = max_x - min_x + 1
    height = max_y - min_y + 1


def init_grid_to_sand():
    global grid
    for i in range(height):
        grid.append([SAND for x in range(width)])

def fill_vertical(x, ys, ye, grid):
    X = x - min_x

    for y in range(ys - min_y, ye+1 - min_y):
        grid[y][X] = CLAY

def fill_horizontal(y, xs, xe, grid):
    y = y - min_y
    for x in range(xs - min_x, xe+1 - min_x):
        grid[y][x] = CLAY

def fill_grid_with_clay(data):
    global grid
    for line in data:
        #x=480, y=133..143
        const, var = line.split(', ')
        const = int(const.split('=')[-1])
        start,end = [int(x) for x in var.split('=')[-1].split('..')]
        isVertical = line.startswith('x=')
        if isVertical:
            fill_vertical(const, start, end, grid)
        else:
            fill_horizontal(const, start, end, grid)

def print_grid(grid, debug=False, sources=None, full=False):
    pad_lines = 4
    if not debug:
        return
    row = [' ' for x in range(500 - min_x)] + ['+'] + [' ' for x in range(max_x - 500)]
    
    print('|', '-'* width, '|', sep='')
    print('|',''.join(row), '|', sep='')
    for y in range(height):
        row = grid[y]
        if not full and not WATER in row:
            if pad_lines == 0:
                return
            pad_lines -= 1
        r = '|'

        for x in range(width):
            c = row[x]
            if sources is not None:
                source = None
                for sx,sy in sources:
                    if sx == x and sy == y:
                        source = 'v'
                        break
                if source is not None:
                    r += source
                    continue
            if c == SAND:
                r += ' '
            elif c == CLAY:
                r += '#'
            elif c == WATER:
                r += '~'
            else:
                r += str(c)

        print(r, '|', sep='')
    print('|', '-'* width, '|', sep='')

def do_fill_and_check(x,y,doneValue,sources, firstFill=True, debug=False):
    if firstFill:
        return do_first_fill_and_check(x,y,doneValue, sources, debug=debug)
    else:
        return do_secondary_fill_and_check(x,y,doneValue, sources, debug=debug)

"""
after the first time we can be above water.
we now have end conditions:
    1. we are outside of the container boundary and below is water - connected to existing source
    2. current space is sand and below is sand - this means new source
    3. current space is water and below is water AND below where we came from is clay - connected to existing source
    4. current space is clay - edge of container reached
    5. ???
"""
def do_secondary_fill_and_check(x,y,doneValue, sources, debug=False):
    c = grid[y][x]
    below = grid[y+1][x]
    xp = x - int(doneValue / abs(doneValue))
    below_previous = grid[y+1][xp]
    if c == SAND:
        grid[y][x] = WATER
        if below == SAND:
            # new source
            sources.append((x,y))
            return doneValue
    elif c == CLAY:
        return doneValue
    elif c == WATER and below == WATER and below_previous == CLAY:
        # existing source
        return doneValue
    return x

"""
first time we're guaranteed to be above clay until we get to sand or water
"""
def do_first_fill_and_check(x,y,doneValue, sources, debug=False):
    c = grid[y][x]
    below = grid[y+1][x]
    # if debug:
    #     print()
    if c == SAND:
        grid[y][x] = WATER
        
        if below == SAND:
            #new source
            sources.append((x,y))
            # don't check left anymore
            x = doneValue
        elif below == WATER:
            # we connected with another source, abandon fill
            x = doneValue
    elif c == CLAY:
        #stop, container edge reached
        x = doneValue
    return x

"""
finds the first row of sand above the shortest (highest y) edge of a container
returns the y value
"""
def get_container_top(x,y):
    # go left/right until we find the edge
    xl = x
    xr = x
    for i in range(width):
        if xl >= 0 and grid[y][xl] == CLAY:
            xl -= 1

        if xr < width and grid[y][xr] == CLAY:
            xr += 1
    xl += 1
    xr -= 1
    yl = y
    yr = y
    # go up until we run out of edge
    for i in range(height):
        if yl > 0 and grid[yl][xl] == CLAY:
            yl -= 1
            
        if yr > 0 and grid[yr][xr] == CLAY:
            yr -= 1
    return min(yl, yr)

def fill_left_and_right(x,y,cl,cr,isFirstFill=False,debug=False):
    sources = []
    xl = x
    xr = x
    if grid[y][x] == SAND:
        grid[y][x] = WATER

    for i in range(width):
        xl -= 1
        xr += 1
        if xl >= 0:
            if xl >= cl:
                xl = do_fill_and_check(xl, y, -1, sources, firstFill=isFirstFill, debug=debug)
            elif grid[y+1][xl] == WATER:
                #connected with another source, list as source and let other systems figure it out
                sources.append((xl,y))
                xl = -1
            elif grid[y+1][xl] == SAND:
                sources.append((xl,y))
                xl = -1
                

        if xr < width:
            if xr <= cr:
                xr = do_fill_and_check(xr, y, width, sources, firstFill=isFirstFill, debug=debug)
            elif grid[y+1][xr] == WATER:
                #connected with another source, list as source and let other systems figure it out
                sources.append((xr,y))
                xr = width
            elif grid[y+1][xr] == SAND:
                sources.append((xr,y))
                xr = width

    return sources

def get_container_left_right(x,y):
    xl = x
    xr = x
    while xl > 0 and grid[y][xl] == CLAY:
        xl -= 1
    while xr < (width-1) and grid[y][xr] == CLAY:
        xr += 1
    return xl+1, xr-1

"""
y+1 is the container

this will generate None, or 1 or 2 sources
"""
def flood_out(x,y, frombottom=True, debug=False):
    # keep for reference
    Y = y
    sources = []
    cl, cr = 0,0
    
    # we want to be able to skip this when we start filling a partially filled container
    if frombottom:
        cl, cr = get_container_left_right(x,y+1)
        # first, fill the bottom (we're here because we hit the bottom)
        if debug:
            print(f"x:{x}, y: {y}")
        sources = fill_left_and_right(x,y,cl,cr,isFirstFill=True)
        if debug:
            print_grid(grid, debug=debug, sources=sources)
            if input() == 'x':
                return None
    else:
        # when not starting at the bottom, find the bottom of this container and set Y to it
        while Y < height and grid[Y][x] != CLAY:
            Y += 1
        Y -= 1
        cl,cr = get_container_left_right(x,Y+1)

    if debug:
        print(f"x:{x}, y: {y}, cl: {cl}, cr: {cr}")

    # when that's done, if we found one or more sources, we're done
    if len(sources) > 0:
        return sources

    # next, find the height of this container
    y = get_container_top(x,Y+1)

    # now from the bottom, go up until we find a fill point
    xl = x - 1
    xr = x + 1
    # Y is bottom, y is top
    for yi in range(Y, y, -1):
        if debug:
            print(f"xl: {xl}, xr: {xr}, yi: {yi}")
        ynext = yi - 1

        
        if debug:
            print('filling left and right')
        sources = fill_left_and_right(x,ynext,cl,cr,isFirstFill=False, debug=debug)
        if debug:
            print_grid(grid, debug=debug, sources=sources)
            if input() == 'x':
                return None

        if len(sources) > 0:
            return sources


    if len(sources) == 0:
        return None
    return sources

def count_water(grid):
    w = 0
    for line in grid:
        w += line.count(WATER)
    return w

def count_contained_water(grid, debug=False):
    grid = dry_up_sources(grid, debug=debug)
    return count_water(grid)

def dry_up_sources(grid, debug=False):
    sources = [[500 - min_x, 0]]
    
    while len(sources) > 0:
        if debug:
            print_grid(grid, debug=True, full=True, sources=sources)
            if input() == 'x':
                return 0

        x,y = sources.pop(0)
        if y >= height or grid[y][x] == SAND:
            continue

        grid[y][x] = SAND
        if grid[y][x-1] != WATER and grid[y][x+1] != WATER:
            sources.append((x, y+1))
            continue

        X = x
        x -= 1
        while grid[y][x] == WATER:
            grid[y][x] = SAND
            x -= 1
        if grid[y][x] == SAND:
            sources.append((x+1, y+1))
        x = X + 1
        while grid[y][x] == WATER:
            grid[y][x] = SAND
            x += 1
        if grid[y][x] == SAND:
            sources.append((x-1, y+1))

    return grid

"""
get here because next space below is water.
the reason the next space is water is either because we have landed back inside a partially filled container
or because we're a secondary stream spilling out of a container
"""
def inside_container(x,y):
    Y = y
    #look down until we hit clay
    while y < height and grid[y][x] != CLAY:
        # if we hit a space directly below that isn't water or clay,
        # we're most likely not inside a container
        if grid[y][x] == SAND:
            return False
        y += 1
    y = Y

    return True

def fill_water(source, debug=False):
    if source is None:
        return None

    x,y = source
    
    if y >= height-1:
        return None

    if grid[y][x] == SAND:
        grid[y][x] = WATER

    next = grid[y+1][x]
    if next == SAND:
        grid[y+1][x] = WATER
        return [[x,y+1]]
    elif next == WATER:
        # we might be part of another source
        if inside_container(x,y):
            sources = flood_out(x,y, frombottom=False, debug=debug)
            return sources

        return None
    else: # next == CLAY:
        sources = flood_out(x,y, debug=debug)
        return sources
    

def part1(debug=False):
    sources = [[500 - min_x, 0]]
    run = 1
    
    while len(sources) > 0:
        if debug:
            print(sources)
        run -= 1
        dd = False
        if run == 0:
            i = None
            if debug:
                i = input('>')
            if i == 'x':
                return
            elif i == 'd':
                dd = True
            else:
                try:
                    run = int(i)
                except:
                    run = 1
        source = sources.pop(0)
        new_sources = fill_water(source, debug=dd)
        if new_sources is not None:
            sources = sources + new_sources
        print_grid(grid, debug=debug, sources=sources)
    
    print_grid(grid, debug=debug, sources=sources)
    w = count_water(grid)
    print ('part 1:')
    print(f"{w} water spaces")
    print(f"should be 30380: {w == 30380}")

def part2(debug=False):
    c = count_contained_water(grid, debug=debug)
    print_grid(grid, debug=debug, full=True)
    print ('part 2:')
    print(f"{c} contained water spaces")
    print(f"should be more than 24969: {c > 24969}")
    print(f"should be 25068: {c == 25068}")


get_min_max(data)
init_grid_to_sand()
fill_grid_with_clay(data)
part1()
print('--------')
part2()
