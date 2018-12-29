#!/usr/bin/env python3

data = None
with open('./18-data.txt') as f:
    data = f.read().splitlines()

OPEN = 0
TREE = 1
YARD = 2

# data = [
#     '.#.#...|#.',
#     '.....#|##|',
#     '.|..|...#.',
#     '..|#.....#',
#     '#.#|||#|#|',
#     '...#.||...',
#     '.|....|...',
#     '||...#|.#|',
#     '|.||||..|.',
#     '...#.|..|.'
# ]
grid = []
ref = []
width = len(data[0])
height = len(data)

for line in data:
    grid.append([])
    ref.append([])
    
    for c in list(line):
        if c == '.':
            grid[-1].append(OPEN)
            ref[-1].append(OPEN)
        elif c == '|':
            grid[-1].append(TREE)
            ref[-1].append(TREE)
        elif c == '#':
            grid[-1].append(YARD)
            ref[-1].append(YARD)

def count_types_around(x,y,t,grid):
    c = 0

    for i in range(-1,2):
        Y = y + i
        if Y < 0 or Y >= height:
            continue
        for j in range(-1,2):
            if i == 0 and j == 0:
                continue
            X = x + j

            if X < 0 or X >= width:
                continue
            a = grid[Y][X]
            if a == t:
                c += 1
    return c

def change_acre(x, y, grid):
    a = grid[y][x]
    # An open acre will become filled with trees 
    if a == OPEN:
        # if three or more adjacent acres contained trees.
        if count_types_around(x,y,TREE, grid) >= 3:
            return TREE
        # Otherwise, nothing happens.

    # An acre filled with trees will become a lumberyard
    elif a == TREE:
        # if three or more adjacent acres were lumberyards.
        if count_types_around(x,y,YARD, grid) >= 3:
            return YARD
        # Otherwise, nothing happens.

    # An acre containing a lumberyard will remain a lumberyard
    elif a == YARD:
        yards = count_types_around(x,y,YARD, grid)
        trees = count_types_around(x,y,TREE, grid)
        # if it was adjacent to at least one other lumberyard 
        # and at least one acre containing trees. 
        if yards == 0 or trees == 0:
            # Otherwise, it becomes open.
            return OPEN
    return a

def update_acres(current, next):
    
    for y in range(height):
        for x in range(width):
            next[y][x] = change_acre(x,y,current)
    return next, current

def printgrid(grid):
    for line in grid:
        o = ''
        for a in line:
            if a == OPEN:
                o += '.'
            elif a == TREE:
                o += '|'
            elif a == YARD:
                o += '#'
            else:
                o += str(a)
        print(o)
    print('')

def count_types(t, grid):
    c = 0
    for line in grid:
        c += line.count(t)
    return c

def get_value(grid):
    trees = count_types(TREE, grid)
    yards = count_types(YARD, grid)
    return trees * yards

#indicies into values array
#these are the indicies that were observed as repeating infinitely in a cycle
x = [
    526, # 567 minutes elapsed is the first complete repeating cycle
    501,
    502,
    503,
    452,
    504,
    505,
    506,
    507,
    508,
    509,
    510,
    511,
    512,
    513,
    514,
    515,
    516,
    396,
    517,
    518,
    519, 
    520, 
    521, 
    522, 
    523, 
    524, 
    525, 
]
def simulate(current, next, minutes):
    # e = list('.......##.')
    # for i in range(width):
    #     print(change_acre(i,0,grid), e[i])
    # print(count_types_around(7, 0, YARD, grid))
    goal = min(minutes, 567)
    elapsed = 0
    values = []
    v = 0
    while minutes > elapsed:
        elapsed += 1
        #this needed to be done before all the checking magic I did...
        # forgot to hit record while doing this :(
        # but at least it was only 15 minutes...
        current, next = update_acres(current, next)
        print(f"processing: {int(elapsed / goal * 100)}%")
        if elapsed == 567:
            print('Prediction is stable now...')
            #28 is the length of the cycle
            val = values[x[(minutes - 567)%28]]
            print(f"expect {minutes} to have value: {val}")
            return val
        
        v = get_value(current)
        # watched these print out and noticed a cycle, thats where 'x' came from above
        # this analysis could probably be automated
        if v in values:
            i = values.index(v)
            if elapsed > 659:
                # print(elapsed, i)
                ii = x[(elapsed - 700)%28]
                if not i == ii:
                    print(f"elapsed: {elapsed}, {i}, v: {v}")
        else:
            if elapsed > 659:
                print(f"NOOOO - elapsed: {elapsed}, v: {v}")
            values.append(v)
        

    #     printgrid(grid)
    printgrid(current)
    
    return v

def part1(grid):
    print('What will the total resource value of the lumber collection area be after 10 minutes?')
    value = simulate(grid, ref, 10)
    print(value)

def part2(grid):
    print('What will the total resource value of the lumber collection area be after 1000000000 minutes?')
    value = simulate(grid, ref, 1000000000)
    print(value)

# part1(grid)
part2(grid)

