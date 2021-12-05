#!/usr/bin/env python3

from typing import List

data = []
with open('./data.txt') as f:
    data = [([int(i) for i in s.split(',')], [int(i) for i in e.split(',')]) for s,e in [l.strip().split(' -> ') for l in f.readlines()]]

def key(p: List[int]) -> str:
    return f'{p[0]:03}|{p[1]:03}'

def step_points(start: List[int],end: List[int]) -> List[int]:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    if dx != 0:
        dx = dx // abs(dx)
    if dy != 0:
        dy = dy // abs(dy)
    while start[0] != end[0] or start[1] != end[1]:
        yield start
        start[0] += dx
        start[1] += dy
    yield end

def part1(d: List[tuple[List[int]]]) -> None:
    pts = {}
    for start,end in d:
        if start[0] == end[0] or start[1] == end[1]:
            for p in step_points(start, end):
                k = key(p)
                pts[k] = pts.get(k, 0) + 1
    s = sum([1 if v > 1 else 0 for v in pts.values()])
    print(f'{s} points have at least 2 lines overlapping')

def part2(d: List[tuple[List[int]]]) -> None:
    pts = {}
    for start,end in d:
        for p in step_points(start, end):
            k = key(p)
            pts[k] = pts.get(k, 0) + 1
    s = sum([1 if v > 1 else 0 for v in pts.values()])
    print(f'{s} points have at least 2 lines overlapping')

# data= [
# ([0,9], [5,9]),
# ([8,0], [0,8]),
# ([9,4], [3,4]),
# ([2,2], [2,1]),
# ([7,0], [7,4]),
# ([6,4], [2,0]),
# ([0,9], [2,9]),
# ([3,4], [1,4]),
# ([0,0], [8,8]),
# ([5,5], [8,2]),
# ]
# part1(data)
part2(data)
