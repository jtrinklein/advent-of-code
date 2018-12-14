#!/usr/bin/env python3

data = None

with open('./13-data.txt') as f:
    data = f.read().splitlines()

carts = 0
pos = []
# the space that this cart is taking up
spacesunder = {}
# current direction of cart by id
dirs = []
def idx(x,y):
    return '|'.join([str(i) for i in [x,y]])

for y in range(len(data)):
    line = list(data[y])
    data[y] = line
    for x in range(len(line)):
        c = line[x]
        if c not in '<>^v':
            continue
        dirs.append(c)
        data[y][x] = str(carts)
        carts += 1
        
        if c in '<>':
            spacesunder[idx(x,y)] = '-'
        elif c in '^v':
            spacesunder[idx(x,y)] = '|'

intersection_choice = [0 for x in range(carts)]

print('carts:', carts)

def get_delta(c):
    if c == '>':
        return 1,0
    if c == '<':
        return -1,0
    if c == '^':
        return 0,-1
    return 0,1

def next_dir(i, n):
    c = get_dir(i)
    if n == '+':
        db = {
            '>': '^>v',
            '<': 'v<^',
            '^': '<^>',
            'v': '>v<'
        }
        
        i = int(i)        
        ic = intersection_choice[i]
        intersection_choice[i]= (ic + 1)%3
        next = db[c][ic]
        # print(i,':', ic, c, next)
        return next

    if c == '>':
        if n == '/':
            return '^'
        else:
            return 'v'
    if c == '<':
        if n == '/':
            return 'v'
        else:
            return '^'
    if c == '^':
        if n == '/':
            return '>'
        else:
            return '<'
    # ELSE c == v
    if n == '/':
        return '<'
    return '>'
    
    

def get_dir(x):
    if x in 'X<>^v/\\+-| ':
        return x
    return dirs[int(x)]

def print_carts(data, debug):
    if not debug:
        return
    for line in data:
        
        print(''.join([get_dir(x) for x in line]))
    print('')


def get_crash(data, debug=False):
    global carts
    done = False
    
    print_carts(data, debug)

    while not done:
        ignore = []
        for y in range(len(data)):
            for x in range(len(data[y])):

                # get current space
                space = data[y][x]
                c = get_dir(space)
                
                if c not in '<>^v':
                    continue
                cid = idx(x,y)

                if cid in ignore:
                    continue

                # get delta
                dx,dy = get_delta(c)
                nx = x + dx
                ny = y + dy
                n = data[ny][nx]

                # if next has cart, we crashed, break out
                if get_dir(n) in '<>^v':
                    #part1
                    # data[ny][nx] = 'X'
                    # print_carts(data, debug)
                    # return ','.join([str(q) for q in [nx,ny]])

                    #part2
                    # replace old spaceunder
                    s = spacesunder[idx(x,y)]
                    data[y][x] = s
                    #replace collided spaceunder
                    s = spacesunder[idx(nx,ny)]
                    data[ny][nx] = s
                    carts -= 2

                    if carts == 1:
                        done = True
                else:
                    # if next is corner
                    #    get next direction
                    if n in '/\\+':
                        c = next_dir(space, n)
                    
                    # replace old spaceunder
                    s = spacesunder[idx(x,y)]
                    data[y][x] = s
                    # save new spaceunder
                    spacesunder[idx(nx,ny)] = n
                    
                    # put new cart down
                    data[ny][nx] = space
                    dirs[int(space)] = c
                    # ignore this cart if we encounter it again
                    ignore.append(idx(nx,ny))
        print_carts(data, debug)
        if debug:
            if input('?') == 'x':
                return 'nope...'
    for i in range(len(data)):
        for j in range(len(data[i])):
            if get_dir(data[i][j]) in '><^v':
                print_carts(data, debug=True)
                return ','.join([str(x) for x in [j,i]])


site = get_crash(data, debug=False)

print(site)
