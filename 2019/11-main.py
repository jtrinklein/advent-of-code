#!/usr/bin/env python3
data = []

with open('./11-data.txt') as f:
    data = [int(x) for x in f.read().split(',')]



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

def rotate_robot(d, how):
    x,y = d
    
    if x == 1:
        if how == 0: # left
            return [0, -1]
        else:
            return [0, 1]
    if x == -1:
        if how == 0: # left
            return [0, 1]
        else:
            return [0, -1]
    if y == 1:
        if how == 0: # left
            return [1, 0]
        else:
            return [-1, 0]
    if y == -1:
        if how == 0: # left
            return [-1, 0]
        else:
            return [1, 0]

def follow_instructions(instructions, pos, direction, points):
    color,turn = instructions
    d = 'left' if turn == 0 else 'right'
    print(f'paint: { color} on {pos}, {len(points)}, turn {d}')
    points[id(pos)] = color
    dx,dy = rotate_robot(direction, turn)
    print(direction, (dx,dy))
    x,y = pos
    
    return [(dx+x, dy+y), (dx,dy)]
    
def id(pos):
    return f'{pos[0]},{pos[1]}'

def run(d, inputs, points):
    
    pos = [0,0]
    direction = [0,-1]
    d += [0]*1000000
    rbase = 0
    pc = 0
    output = []
    
    while pc < len(d):
        opsize = 4
        op = d[pc]
        # print(op)
        [mode1, mode2, mode3] = get_parameter_modes(op)
        op = op % 100
        
        if op == 99: # halt
            opsize = 1 # unnecessary but complete
            print(f'total points painted: {len(points)}')
            return [False, pc, output]

        elif op == 1: # add
            [addr1,addr2,outAddr] = d[pc+1:pc+4]
            # size 4
            v1 = get_param_value(d, addr1, mode1, rbase)
            v2 = get_param_value(d, addr2, mode2, rbase)

            # print(d[pc:pc+4])
            # print(f'add: {v1} + {v2} = {v1+v2} -> [{outAddr}]')
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
            
            # #hand off when unable to read anymore
            # if len(inputs) == 0:
            #     raise 'got an input!'
            addr1 = get_write_address(addr1, mode1, rbase)
            val = points.get(id(pos), 0)
            d[addr1] = val
            

        elif op == 4: # output
            addr1 = d[pc+1]
            v1 = get_param_value(d, addr1, mode1, rbase)
            opsize = 2 

            val = v1
            
            # output val somewhere
            output.append( val)
            if len(output) == 2:
                [p,di] = follow_instructions(output, pos, direction, points)
                pos = p
                direction = di
                output = []
            
        
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

    #part2
def part1():
    run(data, [], {})

def part2():
    points = {}
    points[id((0,0))] = 1
    run(data, [], points)
    pts = [(int(x),int(y)) for x,y in [i.split(',') for i in points.keys()]]
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    for x,y in pts:
        if x < minx:
            minx = x
        if x > maxx:
            maxx = x
        if y < miny:
            miny = y
        if y > maxy:
            maxy = y
    for y in range(miny, maxy+1):
        s = ''
        for x in range(minx, maxx+1):
            p = points.get(id((minx+x,miny+y)),0)
            s += ' ' if p == 0 else '#'
        print(s)
    
part2()        
        