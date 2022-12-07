#!/usr/bin/env python3
from typing import List
data = []
with open('./data.txt') as f:
    data = list(f.read().strip())
    # data = list('mjqjpqmgbljsphdztnvjfqwrcgsmlb')
    # data = list('bvwbjplbgvbhsrlpgdmjqwftvncz')

def get_sopm_idx(stream: List[str], packet_len: int) -> int:
    for i in range(len(stream)-packet_len):
        if len(set(stream[i:i+packet_len])) == packet_len:
            return i + packet_len
    return -1

def part1(stream: List[str]):
    idx = get_sopm_idx(stream, 4)
    print(f'first start of packet marker index: {idx}')

def part2(stream: List[str]):
    idx = get_sopm_idx(stream, 14)
    print(f'first start of message marker index: {idx}')

# part1(data)
part2(data)