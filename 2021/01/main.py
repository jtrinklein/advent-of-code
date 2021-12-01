#!/usr/bin/env python3

data = []
with open('./data.txt') as f:
    data = [int(x) for x in f.readlines()]

def part1(d):
    x = sum([ 1 if a < b else 0 for a,b in zip(d[:-1],d[1:])])
    print(f"{x} increasing measurements")

def part2(d):
    dnew = [x+y+z for x,y,z in zip(d[:-2],d[1:-1],d[2:])]
    part1(dnew)

# part1(data)
part2(data)