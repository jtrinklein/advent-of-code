#!/usr/bin/env python3
data = []

with open('./data.txt') as f:
    # turns this> '3-4 l: vdcv'
    # into this> [3, 4, 'l', 'vdcv']
    data = [[int(i) for i in x.split('-')] + [y[0]] + [z] for x,y,z in [d.split() for d in f.readlines()]]

def validate(min, max, char, pwd):
    c = pwd.count(char)
    return min <= c and c <= max

def xor(a,b):
    return (a or b) and a != b

def validate2(p1, p2, ch, pwd):
    # p1,p2 represent character position not index
    # 1 is first character, thus index 0
    p1 -= 1
    p2 -= 1
    l = len(pwd)
    return p1 < l and p2 < l and xor(pwd[p1] == ch, pwd[p2] == ch)

def get_valid_passwords(d, validator):
    return [pwd for min,max,ch,pwd in d if validator(min,max,ch,pwd)]

def part1(d):
    c = len(get_valid_passwords(d, validate))
    print(f'{c} valid passwords')

def part2(d):
    c = len(get_valid_passwords(d, validate2))
    print(f'{c} valid passwords')

#part1(data)
part2(data)