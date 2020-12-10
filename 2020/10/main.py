#!/usr/bin/env python3

data = []

with open('./data.txt') as f:
    data = [int(line) for line in f.readlines()]

def part1(d):
    d.sort()
    # wall joltage starts at 0
    d = [0] + d 
    diffs = [y-x for x,y in zip(d[:-1], d[1:])]

    ones = diffs.count(1)

    # devices joltage is guaranteed to create a +3
    threes = diffs.count(3) + 1

    print(f'{ones} +1 diffs, {threes} +3 diffs = {ones * threes}')

part1(data)