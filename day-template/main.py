#!/usr/bin/env python3
from time import time

def parse_input(filename: str):
    data = []
    with open(filename) as f:
        data = [x for x in f.readlines()]
    return data

def part1(d):
    pass

def part2(d):
    pass

def run():
    data = parse_input('./test.data.txt')
    start_time = time()
    part1(data)
    # part2(data)
    end_time = time()
    duration = end_time - start_time
    print(f'\nIt took {duration} seconds.')

if __name__ == '__main__':
    run()