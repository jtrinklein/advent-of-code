#!/usr/bin/env python3
from collections import deque
# import platform
# if platform.system() == 'Windows':
#     from msvcrt import getch
# else:
#     #requires: pip install getch
#     from getch import getch

data = []

with open('./15-data.txt') as f:
    data = [int(x) for x in f.read().split(',')]


grid = []
w = 41
h = 41
steps = []
for x in range(h):
    grid.append([0]*w)
    steps.append([None]*w)


unexplored = 0
empty = 1
wall = 2
o2mod = 3

def print_grid(rx,ry, minX,minY, maxX, maxY,g):
    for y in range(minY,maxY + 1):
        line = ''
        for x in range(minX, maxX+1):
            i = g[y][x]
            if x == rx and y == ry: line += '$'
            elif x == 50 and y == 50: line += 'X'
            elif  i == wall: line += '#'
            elif  i == empty: line += '.'
            elif i == o2mod: line += '@'
            else: line += ' '
        print(line)
    print('-')

position_mode = 0
immediate_mode = 1
relative_mode = 2

def get_parameter_modes(op):
    """
     0 == position mode
     1 == immediate mode
     2 == relative mode
    """
    # the first parameter's mode is in the hundreds digit,
    mode1 = (op // 100) % 10
    # the second parameter's mode is in the thousands digit,
    mode2 = (op // 1000) % 10
    # the third parameter's mode is in the ten-thousands digit,
    mode3 = (op // 10000) % 10
    # and so on. 
    return [mode1, mode2, mode3]

def get_param_value(d, val, mode, rbase):
    if mode == immediate_mode:
        return val
    if mode == position_mode:
        return d[val]
    if mode == relative_mode:
        return d[rbase + val]
    raise 'Bad parameter mode'

def get_write_address(val, mode, rbase):
    if mode == relative_mode:
        return rbase + val
    return val


def run(d, inputs, part1):
    
    north = 1
    south = 2
    west = 3
    east = 4
    directions = deque([north, east, south, west])
    adjust_level = 0

    d += [0]*1000
    rbase = 0
    pc = 0
    output = []
    mem_inputs = []
    rx,ry = 21,21
    minX,minY = 0,0
    maxX,maxY = 40,40
    dx,dy = 0,0
    start_visits = 0
    steps[ry][rx] = 0
    while pc < len(d):
        
        opsize = 4
        op = d[pc]
        [mode1, mode2, mode3] = get_parameter_modes(op)
        op = op % 100
        if op == 99: # halt
            opsize = 1 # unnecessary but complete
            # print(output)
            print(mem_inputs)
            return [False, 0, grid]

        elif op == 1: # add
            [addr1,addr2,outAddr] = d[pc+1:pc+4]
            # size 4
            v1 = get_param_value(d, addr1, mode1, rbase)
            v2 = get_param_value(d, addr2, mode2, rbase)

            outAddr = get_write_address(outAddr, mode3, rbase)
            d[outAddr] = v1 + v2

        elif op == 2: # mul
            [addr1,addr2,outAddr] = d[pc+1:pc+4]
            # size 4
            v1 = get_param_value(d, addr1, mode1, rbase)
            v2 = get_param_value(d, addr2, mode2, rbase)
            
            
            outAddr = get_write_address(outAddr, mode3, rbase)
            d[outAddr] = v1 * v2

        elif op == 3: # input
            addr1 = d[pc+1]
            opsize = 2 
            
            up = 72
            right =77
            down = 80
            left = 75
            q = 113


            # print_grid(rx, ry, minX,minY, maxX, maxY, grid)
            # time.sleep(0.015) # ~60fps
            # print('?')
            # k = ord(getch())
            # if k == 224: k = ord(getch()) # arrow keys are 2 bytes
            
            # if k == q:
            #     return [False,0,grid]

            # elif   k == up: 
            #     inputs.append(north) # up
            #     dx,dy = 0,-1

            # elif k == right:
            #     inputs.append(east) # right
            #     dx,dy = 1,0

            # elif k == down:
            #     inputs.append(south) # down
            #     dx,dy = 0,1

            # elif k == left:
            #     inputs.append(west) # left
            #     dx,dy = -1,0

            direction = directions[0]
            if direction == north:
                dx,dy = 0,-1
            elif direction == south:
                dx,dy = 0,1
            elif direction == east:
                dx,dy = 1,0
            elif direction == west:
                dx,dy = -1,0
            
            # if len(inputs) == 0:
            #     raise 'got an input!'
            #     # return [True, pc, output]
            
            addr1 = get_write_address(addr1, mode1, rbase)

            # v = inputs.pop(0)
            # d[addr1] = v
            d[addr1] = direction

        elif op == 4: # output
            addr1 = d[pc+1]
            v1 = get_param_value(d, addr1, mode1, rbase)
            opsize = 2 

            val = v1
            minX = min(rx+dx, minX)
            maxX = max(rx+dx,maxX)
            minY = min(ry+dy, minY)
            maxY = max(ry+dy,maxY)
            # 0: The repair droid hit a wall. Its position has not changed.
            # 1: The repair droid has moved one step in the requested direction.
            # 2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
            if val == 0:
                grid[ry+dy][rx+dx] = wall
                adjust_level += 1
                directions.rotate(-1)
            elif val == 1:
                grid[ry+dy][rx+dx] = empty
                if steps[ry+dy][rx+dx] is None:
                    steps[ry+dy][rx+dx] = steps[ry][rx]+1
                rx += dx
                ry += dy
                if adjust_level > 0:
                    adjust_level -= 1
                    directions.rotate(1)
                if rx == 21 and ry == 21:
                    start_visits += 1
                    if start_visits > 1:
                        print_grid(rx, ry, minX,minY, maxX, maxY, grid)
                        print(maxX - minX, minX, maxX)
                        print(maxY - minY, minY, maxY)
                        return  [True, 0, grid]
            elif val == 2:
                grid[ry+dy][rx+dx] = o2mod
                s = steps[ry][rx]+1
                rx += dx
                ry += dy
                
                if adjust_level > 0:
                    adjust_level -= 1
                    directions.rotate(1)
                if part1:
                    return [True, s, grid]
            
            # output val somewhere
            output.append( val)

        
        elif op == 5: # jump-if-true
            [addr1,addr2] = d[pc+1:pc+3]
            v1 = get_param_value(d, addr1, mode1, rbase)
            v2 = get_param_value(d, addr2, mode2, rbase)
            opsize = 3
            #if the first parameter is non-zero
            if v1 != 0:
                #set the instruction pointer to the value from the second parameter
                pc = v2
                continue

        elif op == 6: # jump-if-false
            [addr1,addr2] = d[pc+1:pc+3]
            v1 = get_param_value(d, addr1, mode1, rbase)
            v2 = get_param_value(d, addr2, mode2, rbase)
            opsize = 3
            #if the first parameter is zero
            if v1 == 0:
                #set the instruction pointer to the value from the second parameter
                pc = v2
                continue

        elif op == 7: # less than
            [addr1,addr2,outAddr] = d[pc+1:pc+4]
            v1 = get_param_value(d, addr1, mode1, rbase)
            v2 = get_param_value(d, addr2, mode2, rbase)
            opsize = 4
            
            outAddr = get_write_address(outAddr, mode3, rbase)
            d[outAddr] = 1 if v1 < v2 else 0

        elif op == 8: # equals
            [addr1,addr2,outAddr] = d[pc+1:pc+4]
            v1 = get_param_value(d, addr1, mode1, rbase)
            v2 = get_param_value(d, addr2, mode2, rbase)
            opsize = 4

            outAddr = get_write_address(outAddr, mode3, rbase)
            d[outAddr] = 1 if v1 == v2 else 0

        elif op == 9: # change relative base
            addr1 = d[pc+1]
            v1 = get_param_value(d, addr1, mode1, rbase)
            opsize = 2
            
            rbase += v1

        else:
            print(f'unknown op: {op} at pc: {pc}')
            return [False,-1,output]
        
        pc += opsize
        
    return [False,-1,output]

def part1(d):
    done, steps, grid = run(d, [], part1=True)
    print(f'steps: {steps}')

# part1(data)

oxygen = -2
o2step = -1
def mark_o2_start(grid):
    for y in range(h):
        for x in range(w):
            if grid[y][x] == o2mod:
                grid[y][x] = oxygen
                return
def flood_oxygen(grid):
    done = False
    minutes = 0
    while not done:
        done = True
        for y in range(h):
            for x in range(w):
                if grid[y][x] == oxygen:
                    if grid[y][x+1] == empty: grid[y][x+1] = o2step
                    if grid[y][x-1] == empty: grid[y][x-1] = o2step
                    if grid[y-1][x] == empty: grid[y-1][x] = o2step
                    if grid[y+1][x] == empty: grid[y+1][x] = o2step

        for y in range(h):
            for x in range(w):
                if grid[y][x] == o2step:
                    done = False
                    grid[y][x] = oxygen
        if not done:
            minutes += 1

    return minutes

def part2(d):
    grid = run(d, [], part1=False)[-1]
    mark_o2_start(grid)
    minutes = flood_oxygen(grid)
    print(f'minutes: {minutes}')

part2(data)