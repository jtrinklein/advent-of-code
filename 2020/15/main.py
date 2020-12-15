#!/usr/bin/env python3

data = []

with open('./data.txt') as f:
    data = [int(n) for n in f.readline().strip().split(',')]

# samples
# data = [0,3,6]
# data = [1,3,2]
# data = [2,1,3]
# data = [1,2,3]

def speak_next(nums):
    last_n = nums[0]
    next_n = nums[1:].index(last_n) + 1 if last_n in nums[1:] else 0
    return next_n

def part1(d):
    d.reverse()
    n = d[0]
    starting_count = len(d)

    for _ in range(starting_count, 2020):
        n = speak_next(d)
        d.insert(0, n)

    print(f'2020th number spoken: {n}')

part1(data[:])

    
