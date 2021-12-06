#!/usr/bin/env python3
from copy import deepcopy

data = []
with open('./data.txt') as f:
    data = [int(x) for x in  f.readline().strip().split(',')]


def simulate_days(fish, total_days):
    days = 0
    new_fish = []
    while days < total_days:
        for i,f in enumerate(fish):
            if f == 0:
                fish[i] = 6
                new_fish.append(8)
            else:
                fish[i] -= 1
        if new_fish:
            fish += new_fish
            new_fish = []
        days += 1
    return len(fish)

def new_fish_dict():
    return {x: 0 for x in range(9)}

def simulate_days_smarter(d, total_days):
    # organizes the number of fish by the time left in their cycle
    fish = new_fish_dict()
    for i in range(9):
        fish[i] += d.count(i)

    # copy to setup for the next day
    fish_new = new_fish_dict()
    for _ in range(total_days):
        #respawn fish on day 0
        # existing fish reset their cycle
        fish_new[6] += fish[0]
        # and spawn new fish 2 days out of cycle
        fish_new[8] += fish[0]

        for cycle in range(1,9):
            # move all fish cycles down one day
            fish_new[cycle-1] += fish[cycle] 
        
        fish = deepcopy(fish_new)
        fish_new = new_fish_dict()

    return sum(fish.values())

def part1(d):
    days = 80
    # fish = simulate_days(d, days)
    fish = simulate_days_smarter(d, days)
    print(f'{days} days: {fish} fish')

def part2(d):
    days = 256
    fish = simulate_days_smarter(d, days)
    print(f'{days} days: {fish} fish')

# data = [3,4,3,1,2]
part1(data)
part2(data)
