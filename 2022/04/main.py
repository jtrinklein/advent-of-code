#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Elf:
    start: int
    end: int

data: List[Tuple[Elf,Elf]] = []

with open('./data.txt') as f:
    data = [[Elf(*[int(z) for z in y.split('-')]) for y in x.strip().split(',')] for x in f.readlines()]

def is_contained_pair(p1: Elf, p2: Elf) -> bool:
    return (p1.start <= p2.start and p1.end >= p2.end) or \
        (p2.start <= p1.start and p2.end >= p1.end)

def part1(d):
    count = 0
    for elf1,elf2 in d:
        if is_contained_pair(elf1, elf2):
            count += 1
    print(f'count of contained pairs: {count}')

def overlaps(e1: Elf, e2: Elf) -> bool:
    return e1.start <= e2.start <= e1.end or \
        e1.start <= e2.end <= e1.end or \
        e2.start <= e1.start <= e2.end or \
        e2.start <= e1.end <= e2.end
def part2(d):
    count = 0
    for elf1,elf2 in d:
        if overlaps(elf1, elf2):
            count += 1
    print(f'count of overlapping pairs: {count}')

# part1(data)
part2(data)