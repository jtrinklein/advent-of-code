#!/usr/bin/env python3
from time import time
from typing import List,Tuple

Section = Tuple[int,int]
Point = Tuple[int,int]
BBox = Tuple[Point,Point]
SensorList = List[BBox]

def parse_input(filename: str) -> SensorList:
    data = []
    with open(filename) as f:
        t = [x.strip().split(' ') for x in f.readlines()]
        data =[(int(z[2][2:-1]),int(z[3][2:-1]),int(z[-2][2:-1]),int(z[-1][2:])) for z in t]

    return data

def get_ordered(v1: int, v2: int) -> Tuple[int,int]:
    return (v1,v2) if v1 <= v2 else (v2,v1)

def get_distance(bb: BBox) -> int:
    x0,x1 = get_ordered(bb[0],bb[2])
    y0,y1 = get_ordered(bb[1],bb[3])
    return (x1-x0) + (y1-y0)

def contains_row(bb: BBox, row: int) -> bool:
    y = bb[1]
    d = get_distance(bb)
    return y-d <= row <= y+d

def get_intersection(bb: BBox, row: int) -> Section:
    d = get_distance(bb)
    y0,y1 = get_ordered(bb[1], row)
    dx = d - (y1 - y0)
    x0 = bb[0] - dx
    x1 = bb[0] + dx
    return x0,x1
    
def part1(data: SensorList, focus_row: int):
    sections: set[int] = set()
    beacons: set[int] = set([bb[2] for bb in data if bb[3] == focus_row])
    for bb in data:
        if contains_row(bb, focus_row):
            start,end = get_intersection(bb, focus_row)
            for x in range(start,end+1):
                if x not in beacons:
                    sections.add(x)
    print(f'impossible spaces = {len(sections)}')


def remove_area(spaces: set[Point], bb: BBox):
    d = get_distance(bb)
    sy = bb[1]
    y0 = sy - d
    y1 = sy + d
    for y in range(y0,y1+1):
        dx = d - (sy - y)
        x0 = bb[0] - dx
        x1 = bb[0] + dx
        for x in range(x0,x1+1):
            p = (x,y)
            spaces.remove(p)

def part2(d: SensorList):
    pass

def run():
    data = parse_input('./data.txt')
    focus_row = 2000000
    start_time = time()
    # part1(data, focus_row)
    part2(data)
    end_time = time()
    
    duration = end_time - start_time
    print(f'\nIt took {duration} seconds.')

if __name__ == '__main__':
    run()