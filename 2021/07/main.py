#!/usr/bin/env python3
from typing import List, Tuple, Callable
import statistics
from math import inf

AggregatorFn = Callable[[int, List[int]], List[int]]

data = []
with open('./data.txt') as f:
    data = [int(x) for x in f.readline().strip().split(',')]

def find_optimal_position(d: List[int], cost_aggregator: AggregatorFn) -> Tuple[int,int]:
    
    mean = round(statistics.mean(d))
    mode = int(statistics.mode(data))

    # use narrowed range to search for optimal position (just kinda guessed at the appropriate range)
    rstart = mean-mode
    rend = mean+mode

    fuel_used = inf
    pos = inf
    for start in range(rstart, rend+1):
        f = sum(cost_aggregator(start, d))
        if f < fuel_used:
            fuel_used = f
            pos = start
    return fuel_used, pos

def part1(d: List[int]) -> None:
    cost_aggregator: AggregatorFn = \
        lambda alignment_position, crab_positions: [
            # fuel cost is distance to alignment position
            abs(c - alignment_position) for c in crab_positions
        ]
    fuel_used, pos = find_optimal_position(d, cost_aggregator)
    print(f'part1 - best: {fuel_used} to get to {pos}')

def part2(d: List[int]) -> None:
    cost_aggregator: AggregatorFn = \
        lambda alignment_position, crab_positions: [
            # fuel cost is sum of the series 1 + 2 + ... + n
            # where n is distance to final position
            n*(n+1)//2 for n in [abs(c - alignment_position) for c in crab_positions]
        ]
    fuel_used, pos = find_optimal_position(d, cost_aggregator)
    print(f'part2 - best: {fuel_used} to get to {pos}')

# data = [16,1,2,0,4,2,7,1,2,14]
part1(data)
part2(data)
