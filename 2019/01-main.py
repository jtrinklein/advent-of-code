#!/usr/bin/env python3
import math
data = None

with open('./01-data.txt') as f:
    data = [int(x) for x in f.read().splitlines()]

# fuel = floor(mass/3) - 2
fuel = 0
# fuel = sum([math.floor(x/3) - 2 for x in data])
for m in data:
    print(f'mass: {m}')
    while True:
        mFuel = math.floor(m/3) - 2
        print(f'fuel for mass: {mFuel}')
        if mFuel <= 0:
            break
        fuel += mFuel
        print(f'fuel total: {fuel}')
        m = mFuel
        print(f'mass of fuel: {m}')

print(f'total fuel requirement: {fuel}')