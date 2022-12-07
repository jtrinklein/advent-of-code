#!/usr/bin/env python3

from collections import deque
from dataclasses import dataclass
from typing import List, Deque

@dataclass
class Instruction:
    num: int
    src: int
    dest: int

stacks: List[List[str]] = []
instructions: List[Instruction] = []

def print_stacks():
    for d in stacks:
        print(d)

    print('-'*20)

with open('./data.txt') as f:
    data = [x for x in f.readlines()]
    stack_data = []
    ins_data: List[str] = []
    current_data = stack_data
    for line in data:
        if not line.strip():
            current_data = ins_data
            continue
        current_data.append(line)
    
    for i in range(int(stack_data[-1].strip()[-1])):
        stacks.append([])
    stack_data = stack_data[:-1]
    stack_data.reverse()
    for d in stack_data:
        bins = [x.strip() for x in d[1:-1:2].replace('  ', ' ').split(' ')]
        
        for i,b in enumerate(bins):
            if not b:
                continue
            stacks[i].append(b)
    for line in ins_data:
        instructions.append(Instruction(*[int(x) for x in line[5:].strip().replace(' from ', ',').replace(' to ', ',').split(',')]))

    print_stacks()

def get_top_stacks(s: List[List[str]]) -> str:
    return ''.join([t[-1] for t in s])

def do_ins(ins: Instruction, s: List[List[str]], flip_order: bool = True) -> None:
    num = ins.num
    src = ins.src - 1
    dest = ins.dest - 1
    crates = s[src][-num:]
    s[src] = s[src][:-num]
    if flip_order:
        crates.reverse()
    s[dest] += crates
        
def part1(ins_list: List[Instruction], stack_list: List[List[str]], flip_order = True):
    for ins in ins_list:
        do_ins(ins, stack_list, flip_order)

    print_stacks()
    msg = get_top_stacks(stack_list)
    print(msg)

def part2(ins_list: List[Instruction], stack_list: List[List[str]]):
    part1(ins_list, stack_list, flip_order=False)


# part1(instructions, stacks)
part2(instructions, stacks)