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

part1(data)

