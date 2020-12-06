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

def count_group_consensus_answers(group, answers):
    for g in group.split('\n'):
        answers = [a for a in answers if a in g]
    return len(answers)

def sum_group_consensus_answers(groups):
    potential_answers = list('abcdefghijklmnopqrstuvwxyz')
    return sum([count_group_consensus_answers(group, potential_answers) for group in groups])

def part2(d):
    c = sum_group_consensus_answers(d)
    print(f'total consensus answers: {c}')

part2(data)