from time import time
from typing import List, Dict, Tuple

Point = Tuple[int,int]
Cave = Dict[Point,str]

SAND = 'o'
ROCK = '#'
AIR = '.'

data = []
with open('data.txt') as f:
    data = f.read().splitlines()


def create_cave(scan_data, part2: bool):
    cave = {}

    # Get the max x and y values
    min_x = 500
    max_x = 0
    max_y = 0
    for path in scan_data:
        for point in path.split(' -> '):
            x, y = point.split(',')
            x = int(x)
            y = int(y)
            if x > max_x:
                max_x = x
            if x < min_x:
                min_x = x
            if y > max_y:
                max_y = y

    if part2:
        max_y += 1
    # Create the cave
    for x in range(min_x, max_x + 1):
        for y in range(max_y + 1):
            cave[(x, y)] = AIR

    # Add the rock to the cave
    for path in scan_data:
        points = path.split(' -> ')
        for p1,p2 in zip(points[:-1],points[1:]):
            x1,y1 = [int(i) for i in p1.split(',')]
            x2,y2 = [int(i) for i in p2.split(',')]
            if x1 > x2:
                x1,x2 = x2,x1
            if y1 > y2:
                y1,y2 = y2,y1
            for y in range(y1, y2+1):
                for x in range(x1, x2+1):
                    cave[(x, y)] = ROCK

    return cave, max_y

def get_sand_start_point():
    return (500,0)

def run_simulation(cave: Cave, part2: bool, max_y: int):
    next_sand = move_sand(cave, get_sand_start_point(), part2, max_y)
    source = get_sand_start_point()
    if part2:
        while cave[source] != SAND:
            # Get the next sand
            next_sand = move_sand(cave, next_sand, part2, max_y)
    else:
        while next_sand is not None:
            # Get the next sand
            next_sand = move_sand(cave, next_sand, part2, max_y)

def is_outside_cave(point: Point, cave: Cave) -> bool:
    return point not in cave

def move_sand(cave: Cave, next_sand: Point, part2: bool, max_y: int):

    # Get the next sand position
    next_sand_x, next_sand_y = next_sand
    down_sand = (next_sand_x,next_sand_y+1)

    if is_outside_cave(down_sand, cave):
        if not part2:
            return None

        if down_sand[-1] > max_y:
            cave[next_sand] = SAND
            return get_sand_start_point()
        else:
            cave[down_sand] = AIR
        
    # Check if the next sand position is unblocked
    if cave[(next_sand_x, next_sand_y + 1)] == AIR:
        # Move the sand down
        return down_sand

    left_sand = (next_sand_x - 1, next_sand_y + 1)
    if is_outside_cave(left_sand, cave):
        if not part2:
            return None

        if left_sand[-1] == max_y:
            cave[left_sand] = SAND
            return get_sand_start_point()
        else:
            cave[left_sand] = AIR

    # Check if the next left sand position is unblocked
    if cave[left_sand] == AIR:
        return left_sand

    right_sand = (next_sand_x + 1, next_sand_y + 1)
    if is_outside_cave(right_sand, cave):
        if not part2:
            return None

        if right_sand[-1] == max_y:
            cave[right_sand] = SAND
            return get_sand_start_point()
        else:
            cave[right_sand] = AIR
    
    if cave[right_sand] == AIR:
        return right_sand

    # all positions are blocked, sand stops here
    cave[(next_sand_x, next_sand_y)] = SAND

    # generate new sand
    return get_sand_start_point()

def print_cave(cave):
    # Get the max x and y values
    min_x = 500

    max_x = 0
    max_y = 0
    for x, y in cave:
        if x > max_x:
            max_x = x
        if x < min_x:
            min_x = x
        if y > max_y:
            max_y = y
    print(f'x: {min_x} - {max_x}')
    print(f'y: 0 - {max_y}')
    # Print the cave
    for y in range(max_y + 1):
        for x in range(min_x, max_x + 1):
            c = '.'
            if (x,y) in cave: 
                c = cave[(x,y)]
            print(c, end='')
        print('')
    print('\n')

def part1(scan_data):
    is_part2 = False
    # Create the cave
    cave,max_y = create_cave(scan_data, is_part2)

    # Run the simulation
    run_simulation(cave, is_part2, max_y)

    # Print the cave
    print_cave(cave)

    sand_tiles = list(cave.values()).count('o')
    print(f'{sand_tiles} tiles of sand at rest')


def part2(scan_data):
    is_part2 = True
    # Create the cave
    cave,max_y = create_cave(scan_data, is_part2)

    # Run the simulation
    run_simulation(cave, is_part2, max_y)

    # Print the cave
    # print_cave(cave)

    sand_tiles = list(cave.values()).count('o')
    print(f'{sand_tiles} tiles of sand at rest')


start_time = time()
# part1(data)
part2(data)
end_time = time()
duration = end_time - start_time
print(f'\nIt took {duration} seconds.')