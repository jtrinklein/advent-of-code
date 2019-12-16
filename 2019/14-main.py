#!/usr/bin/env python3
import math
from collections import deque
data = []

with open('./14-data.txt') as f:
    data = f.read().splitlines()

#ex 1
# data = [
#     '10 ORE => 10 A',
#     '1 ORE => 1 B',
#     '7 A, 1 B => 1 C',
#     '7 A, 1 C => 1 D',
#     '7 A, 1 D => 1 E',
#     '7 A, 1 E => 1 FUEL'
# ]

#ex2
# data = [
#     '9 ORE => 2 A',
#     '8 ORE => 3 B',
#     '7 ORE => 5 C',
#     '3 A, 4 B => 1 AB',
#     '5 B, 7 C => 1 BC',
#     '4 C, 1 A => 1 CA',
#     '2 AB, 3 BC, 4 CA => 1 FUEL'
# ]

# data = [
#     '171 ORE => 8 CNZTR',
#     '7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL',
#     '114 ORE => 4 BHXH',
#     '14 VRPVC => 6 BMBT',
#     '6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL',
#     '6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT',
#     '15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW',
#     '13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW',
#     '5 BMBT => 4 WPTQ',
#     '189 ORE => 9 KTJDG',
#     '1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP',
#     '12 VRPVC, 27 CNZTR => 2 XDBXC',
#     '15 KTJDG, 12 BHXH => 5 XCVML',
#     '3 BHXH, 2 VRPVC => 7 MZWV',
#     '121 ORE => 7 VRPVC',
#     '7 XCVML => 6 RJRHP',
#     '5 BHXH, 4 VRPVC => 5 LTCX'
# ]


recipies = {}

for line in data:
    inputs, outputs = line.split(' => ')
    n, name = outputs.split(' ')
    recipies[name] = { 'amount': int(n), 'requires': {}}
    for n,iname in [x.split(' ') for x in inputs.split(', ')]:
        recipies[name]['requires'][iname] = int(n)

def part1():
    debug = True
    requirements = deque([['FUEL', 1]])
    reserves = {}
    ore_reqs = 0
    while len(requirements) > 0:
        # get the req
        [name, num] = requirements[0]

        # check if req met from res
        res_n = reserves.get(name, 0)
        if res_n >= num:
            # if yes, remove the amount needed from reserves
            reserves[name] = res_n - num
            # and remove req
            requirements.popleft()
        else:
            # if not
            # if its ore, increment the ore counter and add to reserves
            if name == 'ORE':
                ore_reqs += num
                requirements.popleft()
                continue

            # otherwise make it.....

            # get the recipe
            r = recipies[name]
            for iname in r['requires'].keys():
                # add all ingredients as reqs
                i_num = r['requires'][iname]
                requirements.appendleft([iname, i_num])

            # add amount recipe produces to reserves
            reserves[name] = reserves.get(name, 0) + r['amount']

    print(f'requires ore: {ore_reqs}')

def make_fuel(fuel_count):
    debug = False
    requirements = deque([['FUEL', fuel_count]])
    reserves = {}
    ore_reqs = 0
    while len(requirements) > 0:
        # get the req
        [name, num] = requirements[0]

        # check if req met from res
        res_n = reserves.get(name, 0)
        if res_n >= num:
            # if yes, remove the amount needed from reserves
            reserves[name] = res_n - num
            # and remove req
            requirements.popleft()
        else:
            # if not
            # if its ore, increment the ore counter and add to reserves
            if name == 'ORE':
                ore_reqs += num
                requirements.popleft()
                continue

            # otherwise make it.....

            # get the recipe
            r = recipies[name]
            x = math.ceil(num / r['amount'])
            for iname in r['requires'].keys():
                # add all ingredients as reqs
                i_num = r['requires'][iname]*x
                requirements.appendleft([iname, i_num])

            # add amount recipe produces to reserves
            reserves[name] = reserves.get(name, 0) + r['amount']*x
    return ore_reqs
    
def part2():
    max_ores = 1000000000000
    mx = 1000000000000
    mn = 1
    
    mid = 0
    while (mx-mn) > 1:
        mid = (mx + mn)// 2
        ore = make_fuel(mid)
    
        if ore == max_ores:
            print(f'exact! {mid} fuels made')
            break
        elif ore > max_ores:
            mx = mid
        else:
            mn = mid
    print(mx,mn)
    print(f'{mx} use less than reserves? {make_fuel(mx) <= max_ores}')
    print(f'{mn} use less than reserves? {make_fuel(mn) <= max_ores}')
    
    
    
    
    
                
part1()
part2()
