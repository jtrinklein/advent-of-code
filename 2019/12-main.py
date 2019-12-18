#!/usr/bin/env python3
from math import gcd
data = []

with open('./12-data.txt') as f:
    data = f.read().splitlines()

# ex 1 data
# data = [
#     '<x=-1, y=0, z=2>',
#     '<x=2, y=-10, z=-7>',
#     '<x=4, y=-8, z=8>',
#     '<x=3, y=5, z=-1>'
# ]

# ex 2 data
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

def apply_gravity2(p,v):
    v[0] += 1 if p[0] < p[1] else (-1 if p[0] > p[1] else 0)
    v[0] += 1 if p[0] < p[2] else (-1 if p[0] > p[2] else 0)
    v[0] += 1 if p[0] < p[3] else (-1 if p[0] > p[3] else 0)
    
    v[1] += 1 if p[1] < p[0] else (-1 if p[1] > p[0] else 0)
    v[1] += 1 if p[1] < p[2] else (-1 if p[1] > p[2] else 0)
    v[1] += 1 if p[1] < p[3] else (-1 if p[1] > p[3] else 0)

    v[2] += 1 if p[2] < p[0] else (-1 if p[2] > p[0] else 0)
    v[2] += 1 if p[2] < p[1] else (-1 if p[2] > p[1] else 0)
    v[2] += 1 if p[2] < p[3] else (-1 if p[2] > p[3] else 0)

    v[3] += 1 if p[3] < p[0] else (-1 if p[3] > p[0] else 0)
    v[3] += 1 if p[3] < p[1] else (-1 if p[3] > p[1] else 0)
    v[3] += 1 if p[3] < p[2] else (-1 if p[3] > p[2] else 0)

def apply_velocity2(p,v):
    p[0] += v[0]
    p[1] += v[1]
    p[2] += v[2]
    p[3] += v[3]

def same(a,b):
    return a[0] == b[0] and a[1] == b[1] and a[2] == b[2] and a[3] == b[3]

def get_cycles(pa, va):
    px = [p[0] for p in pa]
    px0 = px[:]
    vx = [v[0] for v in va]
    vx0 = vx[:]

    py = [p[1] for p in pa]
    py0 = py[:]
    vy = [v[1] for v in va]
    vy0 = vy[:]

    pz = [p[2] for p in pa]
    pz0 = pz[:]
    vz = [v[2] for v in va]
    vz0 = vz[:]
    c = [None, None, None]
    i = 0
    while c[0] is None or c[1] is None or c[2] is None:
        i += 1
        if c[0] is None:
            apply_gravity2(px, vx)
            apply_velocity2(px, vx)
            c[0] = i if same(px0, px) and same(vx0, vx) else None

        if c[1] is None:
            apply_gravity2(py, vy)
            apply_velocity2(py, vy)
            c[1] = i if same(py0, py) and same(vy0, vy) else None

        if c[2] is None:
            apply_gravity2(pz, vz)
            apply_velocity2(pz, vz)
            c[2] = i if same(pz0, pz) and same(vz0, vz) else None
    return c

def lcm(a,b):
    return a*b//gcd(a,b)

def part2(pos_arr, vel_arr):
    cycles = get_cycles(pos_arr, vel_arr)
    c0,c1,c2 = cycles
    c = lcm(lcm(c0,c1), c2)
    print(cycles)
    print(f'cycles to repeat: {c}')
# part1(pos_arr[:], vel_arr[:])
part2(pos_arr[:], vel_arr[:])
