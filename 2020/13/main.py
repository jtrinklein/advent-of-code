#!/usr/bin/env python3
from math import inf
data = []

with open('./data.txt') as f:
    data = [line.strip() for line in f.readlines()]


def part1(d):
    earliest_time = int(d[0])
    routes = d[1].split(',')

    active_routes = [int(x) for x in routes if x.isnumeric()]
    next_route = None
    closest_time = inf
    for route in active_routes:
        #number of completed route runs before earliest depart time
        runs = earliest_time // route

        # next run departs after earliest time, determine which is soonest
        time_until_next_bus = (runs + 1) * route - earliest_time
        if time_until_next_bus < closest_time:
            next_route = route
            closest_time = time_until_next_bus
        
    print(f'next departing route will be {next_route} departing in {closest_time} minutes')
    print(next_route * closest_time)
    
part1(data)