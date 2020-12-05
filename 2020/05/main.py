#!/usr/bin/env python3
from os import getsid, replace

data = []

with open('./data.txt') as f:
    data = [l.strip() for l in f.readlines()]
    
def get_value_from_bin_code(d, one_val):
    v = 0
    vb = [ 1 if x == one_val else 0 for x in d ]
    vb.reverse()
    for i, b in enumerate(vb):
        v += b*(2**i)
    return v

def get_row(d):
    return get_value_from_bin_code(list(d[:7]), 'B')

def get_column(d):
    return get_value_from_bin_code(list(d[7:]), 'R')

def get_seat_id(d):
    return get_row(d) * 8 + get_column(d)

def part1(seats):
    max_seat = max([get_seat_id(seat) for seat in seats])
    print(max_seat)

def part2(seats):
    seat_ids = [get_seat_id(seat) for seat in seats]
    #first seat id is 0 -> 0*8 + 0
    #last seat id is 1023 -> 127*8 + 7
    for sid in range(1,1023): #remember range ends BEFORE stop value
        if (sid not in seat_ids) and (sid+1 in seat_ids) and (sid-1 in seat_ids):
            print(sid)

part2(data)
