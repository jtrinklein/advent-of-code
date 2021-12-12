#!/usr/bin/env python3

from typing import List, Tuple

def parse_data(use_test_data: bool) -> List[List[int]]:
    data = []
    file = './data.txt'
    if use_test_data:
        file = './test.txt'
    with open(file) as f:
        data = [[int(i) for i in list(x.strip())] for x in f.readlines()]
    return data

def model_step(octopi: List[List[int]], debug: bool = False) -> int:
    '''
    During a single step, the following occurs:

    First, the energy level of each octopus increases by 1.
    Then, any octopus with an energy level greater than 9 flashes. This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent. If this causes an octopus to have an energy level greater than 9, it also flashes. This process continues as long as new octopuses keep having their energy level increased beyond 9. (An octopus can only flash at most once per step.)
    Finally, any octopus that flashed during this step has its energy level set to 0, as it used all of its energy to flash.
    '''
    flashes = 0
    flash_queue: List[Tuple[int,int]] = []
    col_max_idx = len(octopi[0]) - 1
    row_max_idx = len(octopi) - 1
    if debug:
        print_octopi(octopi)
    for y,row in enumerate(octopi):
        for x,o in enumerate(row):
            octopi[y][x] = o + 1
            if octopi[y][x] == 10:
                flash_queue.append((x,y))
    if debug:
        print_octopi(octopi)
    # print(flash_queue)
    for x,y in flash_queue:
        # print(f'flashing: {x},{y}')
        flashes += 1

        x_vals: List[int] = [x]
        y_vals: List[int] = [y]
        if x < col_max_idx: x_vals.append(x+1)
        if x > 0:           x_vals.append(x-1)
        if y < row_max_idx: y_vals.append(y+1)
        if y > 0:           y_vals.append(y-1)
        
        for xn in x_vals:
            for yn in y_vals:
                
                # print(f'increasing: {xn},{yn} from {octopi[yn][xn]} to {octopi[yn][xn]+1}')
                octopi[yn][xn] += 1
                if octopi[yn][xn] > 9 and (xn,yn) not in flash_queue:
                    flash_queue.append((xn,yn))
        
        if debug:
            print_octopi(octopi, flashes)
        
    # print(flash_queue)

    for x,y in flash_queue:
        octopi[y][x] = 0
    return flashes

def print_octopi(octopi: List[List[int]], flashes: int = None) -> None:
    if flashes:
        print(f'_{flashes:2}')
    else:
        print('_')
    for row in octopi:
        r = ''
        for o in row:
            if o == 0:
                r += '(0)'
            elif o == 10:
                r += ' X '
                
            elif o > 10:
                r += ' * '
            else:
                r += f' {o} '
        print(r)
def run_steps(n: int, octopi: List[List[int]]) -> int:
    flashes = 0
    for _ in range(n):
        flashes += model_step(octopi)
    return flashes

def part1(d):
    steps = 100
    flashes = run_steps(steps, d)
    print(f'after: {steps} steps, flashes: {flashes}')


def part2(d):
    target = len(d) * len(d[0])
    step = 0
    while True:
        flashes = model_step(d)
        step += 1
        if flashes == target:
            print(f'all {target} flashed after step: {step}')
            return


data = parse_data(use_test_data=False)
# part1(data)
part2(data)

