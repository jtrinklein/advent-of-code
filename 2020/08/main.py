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

def run_program(d, halt_at_line= -1):
    a = 0
    pc = 0
    old_pc = 0
    ins_tracker = {}
    opcodes = build_opcodes()
    eof = len(d)
    while True:
        if pc == eof:
            print(f'end of file reached!')
            return a, eof
        elif pc == halt_at_line:
            print(f'halted at line {pc}')
            print(f'previous line was: {old_pc}')
            print(f'previous instruction: {d[old_pc]}')
            return a, old_pc
        elif pc in ins_tracker:
            print(f'loop detected at line: {old_pc}')
            print(f'last executed instruction: {d[old_pc]}')
            return a, old_pc
        ins_tracker[pc] = 1
        old_pc = pc
        a, pc = do_ins(d[pc], opcodes, a, pc)

def part1(d):
    a, pc = run_program(d)
    print(f'accumulator: {a}, program counter: {pc}')

def part2(d):
    d_orig = d[:]
    eof = len(d)
    is_eof = lambda x: x == eof

    # run the program
    a, halt_line = run_program(d)

    # did it end at eof?
    if is_eof(halt_line):
        # yes we done
        print(f'worked the first time. a: {a}')
        return
    # no
    # LOOP START
    while True:
        # is the last executed instruction jmp or nop? - REMEMBER THIS LINE NUMBER
        while d[halt_line].startswith('acc'):
            # no
            # run the program and stop one short of last run
            _, halt_line = run_program(d, halt_at_line=halt_line)
            # check the instruction again
        # yes
        # change the instruction jmp <-> nop
        if d[halt_line].startswith('jmp'):
            d[halt_line] = f'nop {d[halt_line].split(" ")[-1]}'
        elif d[halt_line].startswith('nop'):
            d[halt_line] = f'jmp {d[halt_line].split(" ")[-1]}'

        # rerun the program with no halt
        a, pc = run_program(d)

        # did it end at eof?
        if is_eof(pc):
            # yes - we done!
            print(f'fixed it! a: {a}')
            return
        # no - reset the program to original
        d = d_orig[:]

        # set the halt to the line we REMEMBERED
        # run program again and halt at REMEMBERED line
        a, halt_line = run_program(d, halt_at_line=halt_line)
        # LOOP RESTART

part1(data)
print('---------')
part2(data)
