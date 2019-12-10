#!/usr/bin/env python3
data = []

with open('./09-data.txt') as f:
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

def run(d, inputs):
    d += [0]*1000000
    rbase = 0
    pc = 0
    output = []
    
    while pc < len(d):
        opsize = 4
        op = d[pc]
        [mode1, mode2, mode3] = get_parameter_modes(op)
        op = op % 100
        # print(f'---\nop: {op}')
        if op == 99: # halt
            opsize = 1 # unnecessary but complete
            # print(output)
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
            # print(d[pc:pc+4])
            # print(f'mul: {v1} * {v2} = {v1*v2} -> [{outAddr}]')
            outAddr = get_write_address(outAddr, mode3, rbase)
            d[outAddr] = v1 * v2

        elif op == 3: # input
            addr1 = d[pc+1]
            opsize = 2 
            
            # print(f'store: 1 -> [{addr1}]')

            #hand off when unable to read anymore
            if len(inputs) == 0:
                raise 'got an input!'
                # return [True, pc, output]
            
            addr1 = get_write_address(addr1, mode1, rbase)

            v = inputs.pop(0)
            d[addr1] = v
            

        elif op == 4: # output
            addr1 = d[pc+1]
            v1 = get_param_value(d, addr1, mode1, rbase)
            opsize = 2 

            val = v1
            if val != 0:
                print(pc)
            # print(d[pc:pc+2])
            # print(f'get: [{addr1}] -> val = {val}')

            # output val somewhere
            output.append( val)
            # print(val)
            # print('='*10)
            
            ## after output hand off to next amp
        
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


# data = [ 109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 ]  ## makes a copy of itself
# data = [1102,34915192,34915192,7,4,7,99,0] # should output a 16 digit number 
# data = [104,1125899906842624,99] # should output the large number 

# [done,pc,output] = run(data, [1]) # part1
[done,pc,output] = run(data, [2]) # part2
ok = sum([abs(x) for x in output[:-1]]) == 0
if ok:
    print(f'val: {output[-1]}')
else:
    print([x for x in output if x != 0])