#!/usr/bin/env python3

data = []
with open('./data.txt') as f:
    data = [[int(y.strip()) for y in x.split('\n')] for x in f.read().split('\n\n')]

def part1(d):
    most_cals = max([sum(x) for x in d])
    print(f'Most calories carried by an elf: {most_cals}')

def part2(d):
    cal_counts = [sum(x) for x in d]
    cal_counts.sort(reverse=True)
    top_counts = cal_counts[:3]
    print(f'Top 3 calories counts carried by elves: {top_counts}')
    print(f'Total: {sum(top_counts)}')

#part1(data)
part2(data)