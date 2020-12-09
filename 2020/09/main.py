#!/usr/bin/env python3

from itertools import combinations
from collections import deque

data = []

with open('./data.txt') as f:
    data = [int(line) for line in f.readlines()]

def is_XMAS_encoded(p, v):
    return v in [sum(c) for c in combinations(p, 2)]

def part1(d):
    vals = deque()
    preamble_length = 25
    for v in d:
        if len(vals) > preamble_length:
            vals.popleft()

        if len(vals) == preamble_length and not is_XMAS_encoded(vals, v):
            print(f'first non-encoded value: {v}')
            return v

        vals.append(v)

def part2(d):
    target_value = part1(d)
    range_end = d.index(target_value) + 1
    for chain_length in range(2, 26):
        print(f'trying chain length of: {chain_length}')
        for i in range(range_end - chain_length + 1):
            values = d[i : i + chain_length]
            s = sum(values)
            if s == target_value:
                print(f'these values: {values}')
                print(f'sum to this value: {target_value}')
                print(f'sum of smallest and largest is: {min(values) + max(values)}')
                return

part2(data)
