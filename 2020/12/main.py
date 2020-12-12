#!/usr/bin/env python3
from dataclasses import dataclass

@dataclass
class ShipInfo:
    '''
    class for keeping ship's information
    '''

    dir_index: int
    x: int
    y: int
    def __init__(self, x, y, dir_index):
        self.x = x
        self.y = y
        self.dir_index = dir_index

data = []

with open('./data.txt') as f:
    data = [(x[0], int(x[1:])) for x in f.readlines()]

directions = [ 'N', 'E', 'S', 'W' ]
movement = {
    'N': (0,  1),
    'E': (1,  0),
    'S': (0, -1),
    'W': (-1, 0),
}
rotation_direction = {
    'L': -1,
    'R': 1,
}

def move_ship(instruction, magnitude, ship_info):
    # ship can "slide" directions using N,E,S,W instructions - current direction does not matter
    # F depends on direction
    # L is counterclockwise
    if instruction in 'LR':
        dir_changes = rotation_direction[instruction] * ( magnitude // 90 )
        ship_info.dir_index = (ship_info.dir_index + dir_changes) % 4
        return

    move_dir = directions[ship_info.dir_index] if instruction == 'F' else instruction

    dx,dy = [i * magnitude for i in movement[move_dir] ]
    ship_info.x += dx
    ship_info.y += dy

def follow_course(instructions):
    ship_info = ShipInfo(0, 0, directions.index('E'))
    for instruction, magnitude in instructions:
        move_ship(instruction, magnitude, ship_info)
    
    return abs(ship_info.x) + abs(ship_info.y)

def part1(d):
    dist = follow_course(d)
    print(f'final distance: {dist}')

part1(data)

