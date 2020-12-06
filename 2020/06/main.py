#!/usr/bin/env python3
data = []

with open('./data.txt') as f:
    data = f.read().split('\n\n')

def get_group_answers(g):
    return sum([1 for x in 'abcdefghijklmnopqrstuvwxyz' if x in g])

def sum_group_answers(d):
    return sum([get_group_answers(g) for g in d])

def part1(d):
    c = sum_group_answers(d)
    print(f'total answers: {c}')

part1(data)