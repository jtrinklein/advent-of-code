#!/usr/bin/env python3
from sys import intern

data = []
with open('./data.txt') as f:
    data = [(intern(y),int(z)) for y,z in [x.split(' ') for x in f.readlines()]]


def part1(d):
    cmds = {
        intern('forward'): lambda n,d,p: (d, p+n),
        intern('down'): lambda n,d,p: (d+n, p),
        intern('up'): lambda n,d,p: (d-n, p),
    }
    depth = 0
    position = 0
    for cmd,n in d:
        depth, position = cmds[cmd](n, depth, position)

    print(f'd: {depth}, p: {position}, result: {depth*position}')

def part2(d):
    cmds = {
        intern('forward'): lambda n,d,p,a: (d+(a*n), p+n, a),
        intern('down'): lambda n,d,p,a: (d, p, a+n),
        intern('up'): lambda n,d,p,a: (d, p, a-n),
    }
    aim = 0
    depth = 0
    position = 0
    for cmd,n in d:
        depth, position, aim = cmds[cmd](n, depth, position, aim)

    print(f'd: {depth}, p: {position}, a: {aim}, result: {depth*position}')

# part1(data)
part2(data)