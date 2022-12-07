#!/usr/bin/env python3

from typing import List, Dict
data = []
with open('./data.txt') as f:
    data = [list(x.strip()) for x in f.readlines()]

def get_item_counts(d: List[str]) -> Dict[str,int]:
    return  {x: d.count(x) for x in d}

def part1(rucksacks: List[List[str]]):
    dupes = []
    aVal = ord('a')
    AVal = ord('A')
    for rs in rucksacks:
        h = len(rs)//2
        c1 = get_item_counts(rs[0:h])
        c2 = get_item_counts(rs[h:])
        for k in c1:
            if k in c2:
                val = ord(k) - aVal + 1 if k.islower() else ord(k) - AVal + 27
                #print(f'{k} - {val}')
                dupes.append(val)
                break
    
    total = sum(dupes)
    print(f'{total}')

def part2(rucksacks: List[List[str]]):
    dupes = []
    aVal = ord('a')
    AVal = ord('A')
    for i in range(0, len(rucksacks), 3):
        rs1,rs2,rs3 = rucksacks[i:i+3]
        c1 = get_item_counts(rs1)
        c2 = get_item_counts(rs2)
        c3 = get_item_counts(rs3)
        for k in c1:
            if k in c2 and k in c3:
                val = ord(k) - aVal + 1 if k.islower() else ord(k) - AVal + 27
                #print(f'{k} - {val}')
                dupes.append(val)
                break
    
    total = sum(dupes)
    print(f'{total}')

#part1(data)
part2(data)