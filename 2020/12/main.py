#!/usr/bin/env python3
from dataclasses import dataclass

@dataclass
class ShipInfo:
    '''
    class for keeping ship's information
    '''
    wx: int
    wy: int
    dir_index: int
    x: int
    y: int
    def __init__(self, x, y, dir_index, wx = 0, wy = 0):
        self.x = x
        self.y = y
        self.dir_index = dir_index
        self.wx = wx
        self.wy = wy

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

def move_with_waypoint(instruction, magnitude, ship_info):
    '''
    Action N means to move the waypoint north by the given value.
    Action S means to move the waypoint south by the given value.
    Action E means to move the waypoint east by the given value.
    Action W means to move the waypoint west by the given value.
    Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
    Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
    Action F means to move forward to the waypoint a number of times equal to the given value.
    '''
    if instruction in 'LR':
        for _ in range( magnitude // 90 ): # for however many rotations to perform
            # swap wx,wy
            ship_info.wx, ship_info.wy = ship_info.wy, ship_info.wx
            
            if instruction == 'L':
                # invert wx for L rotation
                ship_info.wx *= -1
            else:
                # invert wy for R rotation
                ship_info.wy *= -1
        return

    if instruction == 'F':
        ship_info.x += magnitude * ship_info.wx
        ship_info.y += magnitude * ship_info.wy
        return

    # only NESW left
    dx,dy = movement[instruction]
    ship_info.wx += dx * magnitude
    ship_info.wy += dy * magnitude


def follow_course(instructions, move_function=move_ship):
    ship_info = ShipInfo(0, 0, directions.index('E'), wx=10, wy=1)
    for instruction, magnitude in instructions:
        move_function(instruction, magnitude, ship_info)
    return abs(ship_info.x) + abs(ship_info.y)

def part1(d):
    dist = follow_course(d)
    print(f'final distance: {dist}')

def part2(d):
    dist = follow_course(d, move_function=move_with_waypoint)
    print(f'final distance following waypoint: {dist}')

part2(data)

