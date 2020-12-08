#!/usr/bin/env python3

data = []

with open('./data.txt') as f:
    data = [line.strip() for line in f.readlines()]

def do_ins(line, opcodes, a, pc):
    ins, val = line.split(' ')
    a,pc = opcodes[ins](int(val), a, pc)
    return a, pc

def build_opcodes():
    return {
        'jmp': lambda v,a,pc: (a,     pc + v),
        'acc': lambda v,a,pc: (a + v, pc + 1),
        'nop': lambda v,a,pc: (a,     pc + 1),
    }

def run_program(d, halt_on_loop=True):
    a = 0
    pc = 0
    ins_tracker = {}
    opcodes = build_opcodes()
    while True:
        if pc in ins_tracker and halt_on_loop:
            return a, pc
        ins_tracker[pc] = 1
        a, pc = do_ins(d[pc], opcodes, a, pc)

def part1(d):
    a, pc = run_program(d)
    print(f'accumulator: {a}, program counter: {pc}')

part1(data)