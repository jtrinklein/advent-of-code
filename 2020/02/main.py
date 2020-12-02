#!/usr/bin/env python3
data = []

with open('./data.txt') as f:
    # turns this> '3-4 l: vdcv'
    # into this> [3, 4, 'l', 'vdcv']
    data = [[int(i) for i in x.split('-')] + [y[0]] + [z] for x,y,z in [d.split() for d in f.readlines()]]

def validate(min, max, char, pwd):
    c = pwd.count(char)
    return min <= c and c <= max

def get_valid_passwords(d):
    return [pwd for min,max,ch,pwd in d if validate(min,max,ch,pwd)]

def part1(d):
    c = len(get_valid_passwords(d))
    print(f'{c} valid passwords')

part1(data)