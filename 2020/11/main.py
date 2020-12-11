#!/usr/bin/env python3

data = []

with open('./data.txt') as f:
    data = [list(line.strip()) for line in f.readlines()]

full_seat = '#'
empty_seat = 'L'
floor = '.'

def get_occupied_surrounding(state, x, y, w, h):
    ymin = max(y-1,0)
    ymax = min(y+1,h-1) + 1
    xmin = max(x-1,0)
    xmax = min(x+1, w-1) + 1
    occupied_count = 0
    for yi in range(ymin, ymax):
        for xi in range(xmin, xmax):
            if not (xi == x and yi == y) and state[yi][xi] == full_seat:
                occupied_count += 1
    return occupied_count

def get_next_seat_state(seat, occupied_surrounding):
    '''
    If a seat is empty (L) 
      and there are no occupied seats adjacent to it,
      the seat becomes occupied.
    If a seat is occupied (#)
      and four or more seats adjacent to it are also occupied,
      the seat becomes empty.
    Otherwise, the seat's state does not change.
    '''
    if seat == empty_seat and occupied_surrounding == 0:
        return full_seat
    elif seat == full_seat and occupied_surrounding >= 4:
        return empty_seat

    return seat

def run_one_cycle(state, w, h):
    next_state = []
    for y in range(h):
        next_state.append([floor]*w)
        for x in range(w):
            seat = state[y][x]
            occupied = get_occupied_surrounding(state, x, y, w, h)
            next_state[y][x] = get_next_seat_state(seat, occupied)
    return next_state

def run_cycles(state, w, h):
    cycles = 0
    last_state = None
    
    yield state, cycles
    while state != last_state:
        last_state = state
        state = run_one_cycle(state, w, h)
        cycles += 1
        yield state,cycles

def count_occupied_seats(s):
    return sum([x.count(full_seat) for x in s])

def get_printable_occupied_surrounding(state, x, y, w, h):
    if state[y][x] == floor:
        return ' '
    return str(get_occupied_surrounding(state, x, y, w, h))

def print_layout(state):
    w = len(state[0])
    h = len(state)
    print('------')
    for i,line in enumerate(state):
        count_line = ''.join([get_printable_occupied_surrounding(state, x, i, w, h) for x in range(w)])
        my_line = ''.join(line) 
        print(f"{count_line}   {my_line}")
    print('------')


def part1(d):
    h = len(d)
    w = len(d[0])
    s = None
    for state,round in run_cycles(d, w, h):
        s = state
        print(f'round: {round}')
        # print_layout(state)
        # print(f'occupied: {count_occupied_seats(state)}\n\n')
    print(f'occupied: {count_occupied_seats(s)}\n')

part1(data)