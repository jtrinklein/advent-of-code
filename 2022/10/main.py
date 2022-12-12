#!/usr/bin/env python3
from typing import List, Deque
from collections import deque
data = []
class Operation:
    op: str
    args: List[int]
    def __init__(self, cmd) -> None:
        parts: List[str] = cmd.strip().split(' ')
        self.op = parts[0]
        self.args = [int(x) for x in parts[1:]]

    def do_op(self, regX: int) -> int:
        if self.is_noop():
            return regX
        return regX + self.args[0]
    def is_noop(self) -> bool:
        return self.op == 'noop'

with open('./data.txt') as f:
    data = [Operation(x) for x in f.readlines()]

def part1(d: List[Operation]):
    x = 1
    strength = 0
    c = 0
    pending: Deque[Operation] = deque([])
    while len(d) > 0 or len(pending) > 0:
        c += 1
        if ((c-20) % 40) == 0:
            s = c * x
            strength += s
        
        if len(pending) > 0:
            exec = pending.popleft()
            if exec is not None:
                x = exec.do_op(x)

        elif len(d) > 0:
            op = d.pop(0)
            if not op.is_noop():
                pending.append(op)
    print(f'strength sum: {strength}')

def part2(d):
    x = 1
    strength = 0
    c = 0
    pending: Deque[Operation] = deque([])
    line = ''
    while len(d) > 0 or len(pending) > 0:
        px = c%40
        if x-1 <= px <= x+1:
            line += '#'
        else:
            line += ' '
        c += 1
        if c % 40 == 0:
            print(line)
            line = ''
        
        if len(pending) > 0:
            exec = pending.popleft()
            if exec is not None:
                x = exec.do_op(x)

        elif len(d) > 0:
            op = d.pop(0)
            if not op.is_noop():
                pending.append(op)
        
    print(f'strength sum: {strength}')

# part1(data)
part2(data)