#!/usr/bin/env python3
from itertools import permutations
from collections import deque
data = []

with open('./07-data.txt') as f:
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
    #mode3 = (op // 10000) % 10
    # and so on. 
    return [mode1, mode2]


def run(d, inputs, pc, output):
    
    while pc < len(d):
        opsize = 4
        op = d[pc]
        [mode1, mode2] = get_parameter_modes(op)
        op = op % 100
        # print(f'---\nop: {op}')
        if op == 99: # halt
            opsize = 1 # unnecessary but complete
            # print(output)
            return [False, pc, output]

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

        elif op == 3: # input
            addr1 = d[pc+1]
            opsize = 2 
            # print(d[pc:pc+2])
            # print(f'store: 1 -> [{addr1}]')

            #hand off when unable to read anymore
            if len(inputs) == 0:
                return [True, pc, output]
            d[addr1] = inputs.pop(0)
            

        elif op == 4: # output
            addr1 = d[pc+1]
            v1 = d[addr1] if mode1 == position_mode else addr1
            opsize = 2 

            val = v1
            # print(d[pc:pc+2])
            # print(f'get: [{addr1}] -> val = {val}')

            # output val somewhere
            output = val
            # print(val)
            # print('='*10)
            
            ## after output hand off to next amp
        
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
            return [False,-1,-1]
        
        pc += opsize
        
    return [False,-1,-1]


def part1(data):
    max_thrust = 0
    best_settings= None
    for settings in permutations(range(5)):
        # print(f'testing: {settings}')
        mt = 0
        for s in settings:
            mt = run(data[:], [s, mt])[-1]

        if mt > max_thrust:
            max_thrust = mt
            best_settings = settings[:]
    print(f'max thrust: {max_thrust}, settings: {best_settings}')



def run_continuous(settings, d):
    
    i = 0
    
    programs = [d[:], d[:], d[:], d[:], d[:]]
    ips = [0]*5
    program_running = [True]*5
    outputs = [0]*5
    inputs = [[s]  for s in settings[:]]
    inputs[0].append(0)
    # print(inputs)
    while program_running[-1]: # run until E halts
        
        
        # print('ABCDE'[i], programs[i][-3:], inputs[i])
        status = run(programs[i], inputs[i], ips[i], outputs[i])
        [running, ip, output] = status
        program_running[i] = running
        outputs[i] = output
        inputs[(i+1)%5].append(output)
        ips[i] = ip
        # print('ABCDE'[i], programs[i][-3:], inputs[i])

        #print('ABCDE'[i], status, programs[i][-3:], inputs[i], ips)

        i = (i + 1) % 5
    return outputs[-1]

def part2(data):
    max_thrust = 0
    best_settings= None
    for settings in permutations(range(5,10)):
        # print(f'testing: {settings}')
        result = run_continuous(settings, data)  
        if result > max_thrust:
            max_thrust = result
            best_settings = settings[:]
    print(f'max thrust: {max_thrust}, settings: {best_settings}')

part2(data)
# print('expect: 139629729, settings [9,8,7,6,5]')
# prog = [
#     3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
# ]
# print(f'result: {run_continuous([9,8,7,6,5], prog)}')
# part2([
#     3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
# ])
# print('expect: 18216, settings [9,7,8,5,6]')
# part2([
#     3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
# ])

