#!/usr/bin/env python3
from collections import deque
from typing import List

DEBUG_LOGGING = False
data = []
with open('./data.txt') as f:
# with open('./test.txt') as f:
    data = [[int(i) for i in list(x.strip())] for x in f.readlines()]

def print_map(d: List[List[int]], stripval: int = None) -> None:
    if not DEBUG_LOGGING:
        return
    for line in d:
        print(''.join([' ' if stripval and x == stripval else str(x) for x in line]))
    print('-------------------')

def get_risk(d: List[List[int]]) -> int:
    risk: int = 0
    x_min, x_max = 0,len(d[0])-1
    y_min, y_max = 0,len(d)-1
    for y,row in enumerate(d):
        for x,v in enumerate(row):
            if x > x_min and v >= row[x-1]:
                continue
            if x < x_max and v >= row[x+1]:
                continue
            if y > y_min and v >= d[y-1][x]:
                continue
            if y < y_max and v >= d[y+1][x]:
                continue
            risk += v+1
    return risk

def fill_basin(x0: int, x_max: int, y0: int, y_max: int, travel_map: List[List[int]]) -> int:
    points = deque([(x0,y0)])
    count = 1
    size = 0
    while count > 0:
        x,y = points.pop()
        count -= 1
        if travel_map[y][x] == 0:
            travel_map[y][x] = 2
            size += 1
            if x > 0 and travel_map[y][x-1] == 0:
                points.appendleft((x-1,y))
                count += 1
            if x < x_max and travel_map[y][x+1] == 0:
                points.appendleft((x+1,y))
                count += 1
            if y > 0 and travel_map[y-1][x] == 0:
                points.appendleft((x,y-1))
                count += 1
            if y < y_max and travel_map[y+1][x] == 0:
                points.appendleft((x,y+1))
                count += 1
    return size

def get_basins(d: List[List[int]]) -> List[int]:
    travel_map = [[0 if v != 9 else 1 for v in x] for x in d]
    print_map(travel_map)
    x_max = len(d[0])-1
    y_max = len(d)-1
    basin_sizes = []
    for y in range(y_max+1):
        for x in range(x_max+1):
            if travel_map[y][x] == 0:
                size = fill_basin(x, x_max, y, y_max, travel_map)
                basin_sizes.append(size)
    print_map(travel_map, stripval=1)
    basin_sizes.sort(reverse=True)
    return basin_sizes

def part1(d: List[List[int]]):
    risk = get_risk(d)
    print(f'risk: {risk}')

def part2(d):
    print_map(d)
    basins = get_basins(d)
    print(basins)
    v = basins[0] * basins[1] * basins[2]
    print(f'identified {len(basins)}. top three: {basins[:3]}. product: {v}')

# part1(data)
part2(data)

