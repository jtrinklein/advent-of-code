#!/usr/bin/env python3
data = []

with open('./05-data.txt') as f:
    data = [int(x) for x in f.read().split(',')]

# data = [
#     1002,4,3,4,33
# ]

position_mode = 0
immediate_mode = 1
def get_parameter_modes(op):
    """
     0 == position mode
     1 == immediate mode
    """
    # the first parameter's mode is in the hundreds digit,
    mode1 = (op // 100) % 10
    # the second parameter's mode is in the thousands digit,
    mode2 = (op // 1000) % 10
    # the third parameter's mode is in the ten-thousands digit,
    mode3 = (op // 10000) % 10
    # and so on. 
    return [mode1, mode2, mode3]

# def run(noun, verb, d):
def run(d):
    # program overrides:
    # d[1] = noun
    # d[2] = verb
    pc = 0
    output = [0]
    while pc < len(d):
        opsize = 4
        op = d[pc]
        [mode1, mode2, mode3] = get_parameter_modes(op)
        op = op % 100
        # print(f'---\nop: {op}')
        if op == 99: # halt
            opsize = 1 # unnecessary but complete
            return output

        elif op == 1: # add
            [addr1,addr2,outAddr] = d[pc+1:pc+4]
            # size 4
            v1 = d[addr1] if mode1 == position_mode else addr1
            v2 = d[addr2] if mode2 == position_mode else addr2
            # print(d[pc:pc+4])
            # print(f'add: {v1} + {v2} = {v1+v2} -> [{outAddr}]')
            d[outAddr] = v1 + v2

        elif op == 2: # mul
            [addr1,addr2,outAddr] = d[pc+1:pc+4]
            # size 4
            v1 = d[addr1] if mode1 == position_mode else addr1
            v2 = d[addr2] if mode2 == position_mode else addr2
            # print(d[pc:pc+4])
            # print(f'mul: {v1} * {v2} = {v1*v2} -> [{outAddr}]')
            d[outAddr] = v1 * v2

        elif op == 3: # store
            addr1 = d[pc+1]
            opsize = 2 
            # print(d[pc:pc+2])
            # print(f'store: 1 -> [{addr1}]')

            # part1
            # d[addr1] = 1
            d[addr1] = 5

        elif op == 4: # retrieve
            addr1 = d[pc+1]
            v1 = d[addr1] if mode1 == position_mode else addr1
            opsize = 2 

            val = v1
            # print(d[pc:pc+2])
            # print(f'get: [{addr1}] -> val = {val}')

            # output val somewhere
            output.append(val)
            print(val)
            # print('='*10)
        elif op == 5: # jump-if-true
            [addr1,addr2] = d[pc+1:pc+3]
            v1 = d[addr1] if mode1 == position_mode else addr1
            v2 = d[addr2] if mode2 == position_mode else addr2
            opsize = 3
            #if the first parameter is non-zero
            if v1 != 0:
                #set the instruction pointer to the value from the second parameter
                pc = v2
                continue

        elif op == 6: # jump-if-false
            [addr1,addr2] = d[pc+1:pc+3]
            v1 = d[addr1] if mode1 == position_mode else addr1
            v2 = d[addr2] if mode2 == position_mode else addr2
            opsize = 3
            #if the first parameter is zero
            if v1 == 0:
                #set the instruction pointer to the value from the second parameter
                pc = v2
                continue

        elif op == 7: # less than
            [addr1,addr2,outAddr] = d[pc+1:pc+4]
            v1 = d[addr1] if mode1 == position_mode else addr1
            v2 = d[addr2] if mode2 == position_mode else addr2
            opsize = 4
            
            d[outAddr] = 1 if v1 < v2 else 0

        elif op == 8: # equals
            [addr1,addr2,outAddr] = d[pc+1:pc+4]
            v1 = d[addr1] if mode1 == position_mode else addr1
            v2 = d[addr2] if mode2 == position_mode else addr2
            opsize = 4
            
            d[outAddr] = 1 if v1 == v2 else 0

        else:
            print(f'unknown op: {op} at pc: {pc}')
            return [9,9,9]
        pc += opsize
    return [9,9,9]

out = run(data)
# checksum = sum(out[:-1])
# success = checksum == 0
# print(f'success: {success}, code: {out[-1]}')
print(f'code: {out[-1]}')