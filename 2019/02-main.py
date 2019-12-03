#!/usr/bin/env python3

data = None

with open('./02-data.txt') as f:
    data = [int(x) for x in f.read().split(',')]



def run(noun, verb, d):
    # program overrides:
    d[1] = noun
    d[2] = verb
    pc = 0
    while pc < len(d):
        [op,addr1,addr2,outAddr] = d[pc:pc+4]
        if op == 99:
            return d[0]
        elif op == 1:
            d[outAddr] = d[addr1] + d[addr2]
        elif op == 2:
            d[outAddr] = d[addr1] * d[addr2]
        else:
            print(f'unknown op: {op} at pc: {pc}')
        pc += 4

def find_inputs():
    for i in range(100):
        for j in range(100):
            d = data[:]

            result = run(i, j, d)
            if result == 19690720:
                print(f'noun: {i}, verb: {j}, value: {i*100 + j}')

find_inputs()
# print(f'finished running, data[0] = {result}')
# op 1 = add
# args inaddr, inaddr, outaddr

# op 2 = multiply
# args inaddr, inaddr, outaddr

# op 99 = halt and catch fire
