#!/usr/bin/env python3

data = []

with open('./17-data.txt') as f:
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


def run(d, inputs, part1):
    d += [0]*10000
    rbase = 0
    pc = 0
    output = ''
    if not part1:
        d[0] = 2
    while pc < len(d):
        
        opsize = 4
        op = d[pc]
        [mode1, mode2, mode3] = get_parameter_modes(op)
        op = op % 100
        if op == 99: # halt
            opsize = 1 # unnecessary but complete
            
            return output

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
            v = 0
            addr1 = get_write_address(addr1, mode1, rbase)
            if not part1:
                if len(inputs[0]) == 0:
                    inputs.pop(0)
                v = inputs[0].pop(0)

            d[addr1] = v

        elif op == 4: # output
            addr1 = d[pc+1]
            v1 = get_param_value(d, addr1, mode1, rbase)
            opsize = 2 

            val = v1
            
            # output val somewhere
            if part1:
                output += chr(val)
            else:
                if val < 255:
                    output += chr(val)
                else:
                    output = val
        
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
            return 'unknown op'
        
        pc += opsize
        
    return 'abnormal termination'


def part1(d):
    cv = [list(x) for x in run(d, [], part1=True).strip().splitlines()]
    h = len(cv)
    w = len(cv[0])
    scaffold = '#'
    intersection = 'O'
    s = 0
    for y in range(1, h-1):
        for x in range(1, w-1):
            if cv[y][x] == scaffold:
                i = 0
                i += 1 if cv[y][x+1] == scaffold else 0
                i += 1 if cv[y][x-1] == scaffold else 0
                i += 1 if cv[y+1][x] == scaffold else 0
                i += 1 if cv[y-1][x] == scaffold else 0
                if i > 2:
                    s += x*y
                    cv[y][x] = intersection
    
    print('\n'.join([''.join(x) for x in cv]))
    print(f'sum: {s}')

def part2(d):
    inputs = [
        [ord(x) for x in list('A,B,A,B,A,C,B,C,A,C\n')],
        [ord(x) for x in list('R,4,L,10,L,10\n')],          #A
        [ord(x) for x in list('L,8,R,12,R,10,R,4\n')],      #B
        [ord(x) for x in list('L,8,L,8,R,10,R,4\n')],       #C
        [ord('n'), ord('\n')]
    ]
    dust = run(d, inputs, part1=False)
    print(f'dust collected: {dust}')

part2(data)

