#!/usr/bin/env python3

data = []

with open('./12-data.txt') as f:
    data = f.read().splitlines()
# data = [
#     '<x=-8, y=-10, z=0>',
#     '<x=5, y=5, z=10>',
#     '<x=2, y=-7, z=3>',
#     '<x=9, y=-8, z=-3>'
# ]
pos_arr = []
vel_arr = []
for d in data:
    pos = [int(n.split('=')[-1]) for n in d[1:-1].split(', ')]
    pos_arr.append(pos)
    vel_arr.append([0,0,0])

def apply_gravity(pos_arr, vel_arr):
    for i in range(len(pos_arr)):
        a = pos_arr[i]
        for j in range(len(pos_arr)):
            if i == j:
                continue
            b = pos_arr[j]
            for k in range(3):
                if a[k] == b[k]:
                    d = 0
                elif a[k] < b[k]:
                    d = 1
                else:
                    d = -1
                vel_arr[i][k] += d

def apply_velocity(pos_arr, vel_arr):
    for i in range(len(pos_arr)):
        for j in range(3):
            pos_arr[i][j] += vel_arr[i][j]

def tick(pos_arr, vel_arr):
    apply_gravity(pos_arr, vel_arr)
    apply_velocity(pos_arr, vel_arr)

def printstuff(pos_arr, vel_arr, t):
    print(f'\nAfter {t} steps:')
    for i in range(len(pos_arr)):
        print(f'pos={pos_arr[i]}, vel={vel_arr[i]}')
        
def get_abs_sum(p):
    return sum([abs(x) for x in p])

def get_energy(p,v):
    return get_abs_sum(p) * get_abs_sum(v)

def simulate_steps(pos_arr, vel_arr, stepcount):
    t = 0
    # printstuff(pos_arr, vel_arr, t)
    while t < stepcount:
        tick(pos_arr, vel_arr)
        t += 1
        # printstuff(pos_arr, vel_arr, t)

    return sum([get_energy(p, v) for p,v in zip(pos_arr, vel_arr)])

def part1(pos_arr, vel_arr):
    print(simulate_steps(pos_arr, vel_arr, 1000))

def id(pos_arr, vel_arr):
    return ''.join([
        ''.join(str(x).replace(' ','')) for x in pos_arr + vel_arr
    ])

def part2(pos_arr, vel_arr):
    hist ={}
    t = 0
    while not hist.get(id(pos_arr,vel_arr), False):
        i = id(pos_arr, vel_arr)
        hist[i] = True
        tick(pos_arr, vel_arr)
        t += 1
        if t%1000000 == 0:
            print('.')
    print(f'steps: {t}')
# part1(pos_arr[:], vel_arr[:])
part2(pos_arr[:], vel_arr[:])
