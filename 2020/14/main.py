#!/usr/bin/env python3
from math import inf
data = []

with open('./data.txt') as f:
    data = [line.strip() for line in f.readlines()]


def update_mask(bits):
    set_mask = clear_mask = 0
    offset = len(bits)-1
    for i,b in enumerate(bits):
        if b == '1':
            set_mask |= 1 << (offset - i)
        elif b == '0':
            clear_mask |= 1 << (offset - i)
    return set_mask, clear_mask

def store_value(value, addr, mem, set_mask, clear_mask):
    mem[addr] = (int(value) & ~clear_mask) | set_mask

def run_program(instructions):
    set_mask = clear_mask = 0
    mem = {}
    for line in instructions:

        addr, value = line.split(' = ')
        # mask = X01X1XX01011X00110XX011100000111X01X
        if addr.startswith('mask'):
            set_mask, clear_mask = update_mask(value)

        # mem[20234] = 1730
        else:
            # dont need to get the number out of addr, its a unique key
            store_value(value, addr, mem, set_mask, clear_mask)
    return sum(mem.values())

def part1(d):
    value = run_program(d)
    print(f'final value: {value}')

part1(data)
