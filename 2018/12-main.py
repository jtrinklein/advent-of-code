#!/usr/bin/env python3

data = None

with open('./12-data.txt') as f:
    data = f.read().splitlines()
# compare = [
#     '...#...#....#.....#..#..#..#...........',
#     '...##..##...##....#..#..#..##..........',
#     '..#.#...#..#.#....#..#..#...#..........',
#     '...#.#..#...#.#...#..#..##..##.........',
#     '....#...##...#.#..#..#...#...#.........',
#     '....##.#.#....#...#..##..##..##........',
#     '...#..###.#...##..#...#...#...#........',
#     '...#....##.#.#.#..##..##..##..##.......',
#     '...##..#..#####....#...#...#...#.......',
#     '..#.#..#...#.##....##..##..##..##......',
#     '...#...##...#.#...#.#...#...#...#......',
#     '...##.#.#....#.#...#.#..##..##..##.....',
#     '..#..###.#....#.#...#....#...#...#.....',
#     '..#....##.#....#.#..##...##..##..##....',
#     '..##..#..#.#....#....#..#.#...#...#....',
#     '.#.#..#...#.#...##...#...#.#..##..##...',
#     '..#...##...#.#.#.#...##...#....#...#...',
#     '..##.#.#....#####.#.#.#...##...##..##..',
#     '.#..###.#..#.#.#######.#.#.#..#.#...#..',
#     '.#....##....#####...#######....#.#..##.'
# ]
initial = data.pop(0).split(': ').pop()
data.pop(0)
rules = {}

for line in data:
    rule, result = line.split(' => ')
    rules[rule] = result

def get_generation(initial, generations):
    lowest = -5
    initial = '.....' + initial + '.....'
    
    for gen in range(generations):
        next = ''
        count = len(initial)
        for i in range(count):
            start = max(0, i-2)
            end = min(count, i+3)
            val = initial[start:end]
            if i == 0:
                val = '..' + val
            if i == 1:
                val = '.' + val
            if i == count - 2:
                val += '.'
            if i == count - 1:
                val += '..'

            next += rules.get(val, '.')

        if '#' not in next[:7]:
            next = next[1:]
            lowest += 1
        if '#' in next[-5:]:
            next += '.....'
            
        initial = next
    return lowest, initial

def get_sum(lowest, data):
    return sum([x + lowest for x in range(len(data)) if data[x] == '#'])
def part_1(initial):
    lowest, data = get_generation(initial, 20)
    s = get_sum(lowest, data)
    print('part1',s)

def part_2(initial):
    goal = 50000000000
    generations = 1000
    lowest, data = get_generation(initial, generations)
    lowest += goal - generations
    s = get_sum(lowest, data)
    print('part2', s)

part_1(initial)
part_2(initial)