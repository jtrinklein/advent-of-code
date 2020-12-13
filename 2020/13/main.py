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
    
def part2(d):
    routes = d[1].split(',')
    route_delays = [[int(route), route_delay] for route_delay, route in enumerate(routes) if route != 'x']
    # start at time 0
    timestamp = 0
    # start by incrementing by 1
    time_increment = 1

    for route, route_delay in route_delays:
        print(f'time: {timestamp}, route: {route}, delay: {route_delay}, inc: {time_increment}')
        # until the time overlaps the route by the required delay
        # add the increment to the time
        # ex: route 7, delay 1; route 13, delay 2 ; route 17, delay 16
        #  0 %  7 = 0
        #  1 %  7 = 1 < this matches criteria
        # now update the increment by multiplying the increment and this route number
        # inc = inc * 7 = 1 * 7 = 7
        #  1 % 13 = 1
        #  8 % 13 = 8
        # 15 % 13 = 2 < this time stamp matches criteria
        # update increment again
        # inc = inc * 13 = 7 * 13 = 91
        #  15 % 17 = 15
        # 106 % 17 = 4
        # 197 % 17 = 10
        # 288 % 17 = 16 < match! also 288%13 == 2 and 288%7 == 1

        #while (timestamp%route) != route_delay:
        # this ^ doesnt work because if you have a delay greater than the bus id it will never end
        # we can change this to: (time + delay)% route != 0
        # which is equivalent but allows for delays greater than route number

        while (timestamp+route_delay)%route != 0:
            #print(f't: {timestamp} % {route} = {timestamp%route} == {route_delay}')
            timestamp += time_increment
        
        time_increment *= route

    print(timestamp)

part2(data)