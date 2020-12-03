#!/usr/bin/env python3
data = []


with open('./data.txt') as f:
    data = [line.strip() for line in f.readlines()]

def is_tree(i, line):
    return line[i] == '#'

def count_trees_on_trajectory(x0, y0, dx, dy, lines):
    c = 0
    x = x0
    h = len(lines)
    w = len(lines[0])
    for y in range(y0, h, dy):
        if is_tree(x % w, lines[y]): c += 1
        x += dx
    return c

def part1(d):
    c = count_trees_on_trajectory(0,0, 3, 1, d)
    print(f'encountered {c} trees')

def part2(d):
    product = 1
    trajectories= [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    for dx,dy in trajectories:
        c = count_trees_on_trajectory(0,0, dx, dy, d)
        print(f'({dx}, {dy}) encountered {c} trees')
        product *= c
    print(f'result = {product}')

part2(data)

