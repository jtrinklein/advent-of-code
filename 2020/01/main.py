#!/usr/bin/env python3

data = []
with open('./data.txt') as f:
    data = [int(x) for x in f.readlines()]

def get_summands(d, goal):
    for i in range(len(d)):
        x = d[i]
        for y in d[:i]+d[i+1:]:
            if x + y == goal:
                return x,y
    return None,None

def get_summands_recursive(d, goal, count, candidates=[]):
    total = sum(candidates)
    if total > goal:
        return None
    elif len(candidates) == count:
        if total == goal:
            return candidates
        return None
    
    for i in range(len(d)):
        x = d[i]
        result = get_summands_recursive(d[:i]+d[i+1:], goal, count, candidates=candidates+[x])
        if result:
            return result

    return None

def part1():
    x,y = get_summands_recursive(data, 2020, 2)
    if x and y:
        print(f'{x} * {y} = {x*y}')

def part2():
    x,y,z = get_summands_recursive(data, 2020, 3)
    if x and y and z:
        print(f'{x} * {y} * {z} = {x*y*z}')

part2()