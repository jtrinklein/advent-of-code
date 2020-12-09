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
            return

        vals.append(v)

part1(data)
