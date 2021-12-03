#!/usr/bin/env python3
from math import ceil

data = []
with open('./data.txt') as f:
    data = [[int(y) for y in list(x.strip())] for x in f.readlines()]

def part1(d):
    lines = len(d)
    bits = len(d[0])
    gamma = 0
    epsilon = 0
    for i in range(bits):
        bit = round(sum([x[i] for x in d])/lines)
        powerOf2 = 2**(bits - (i+1))
        gamma += powerOf2 * bit
        epsilon += powerOf2 * (1-bit)

    print(f'gamma: {gamma}')
    print(f'epsilon: {epsilon}')
    print(f'result: {gamma*epsilon}')

def filter_values(values, use_most_common=True):
    bits = len(values[0])
    for i in range(bits):
        half_value = ceil(len(values) / 2)
        ones_count = 0
        ones = []
        zeros = []
        for v in values:
            ones_count += v[i]
            if v[i] == 1:
                ones.append(v)
            else:
                zeros.append(v)
        bit = ones_count >= half_value
        if not use_most_common:
            bit = not bit
        if bit:
            values = ones[:]
        else:
            values = zeros[:]
        if len(values) == 1:
            return values[0]
    if len(values) > 1:
        raise ValueError("should not have more than one value left")
    return values

def part2(d):
    o2_value  = int(''.join([str(x) for x in filter_values(d[:]) ]), 2)
    co2_value = int(''.join([str(x) for x in filter_values(d[:], use_most_common=False) ]), 2)
    print(f'o2: {o2_value}')
    print(f'co2: {co2_value}')
    print(f'result: {o2_value*co2_value}')
    
#part1(data)
part2(data)

