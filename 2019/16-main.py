#!/usr/bin/env python3
from collections import deque

data = []

with open('./16-data.txt') as f:
    data = f.read()

# data = '34040438'

data = [int(x) for x in list(data)]


def compute_digit(out_pos, inputs):
    pattern = deque([0, 1, 0, -1])
    out = 0
    x = 1
    for d in inputs:
        if x > out_pos:
            pattern.rotate(-1)
            x = 0
        
        out += d*pattern[0]
        x += 1
    # print(line)
    return int(str(out)[-1])

num_digits = len(data)
def get_next_inputs(d,next_digits):
    for i in range(num_digits):
        next_digits[i] = compute_digit(i, d)
    return next_digits
    

def fft(count, d, skip):
    x = d[:]
    y = d[:]
    switch = True
    final = None

    for i in range(count):
        x = get_next_inputs(x,y)
        
    return ''.join([str(c) for c in x[skip:skip+8]])

def part1(d):
    digits = fft(100, d[:], 0)
    print(f'first 8: {digits}')

def part2(data):

    skip = int(''.join([str(x) for x in data[:7]]))
    d = (data*10000)[skip:]
    for _ in range(100):
        s = 0
        for i in range(len(d)-1, -1, -1):
            s = (s + d[i]) % 10
            d[i] = s

    digits = ''.join([str(c) for c in d[:8]])
    print(f'message: {digits}')

part1(data)
part2(data)