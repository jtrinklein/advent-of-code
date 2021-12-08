#!/usr/bin/env python3

from typing import Tuple, List, Dict
from itertools import permutations

data = []
with open('./data.txt') as f:
# with open('./test.txt') as f:
    data = [[d.strip().split(' '), v.strip().split(' ')] for d,v in [l.split(' | ') for l in f.readlines()]]

digit_signals = [ 'abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']

def get_mapped_digit(digit: str, signal_map: Dict[str,str]) -> str:
    v = [signal_map[x] for x in list(digit)]
    v.sort()
    s = ''.join(v)
    if s in digit_signals:
        return digit_signals.index(s)
    return None

def gen_all_maps() -> List[Dict[str,str]]:
    alpha = list('abcdefg')
    maps = []
    for p in permutations(alpha):
        maps.append({a:b for a,b in zip(alpha,p)})
    return maps

def get_correct_mapping(digits: List[str], all_maps: List[Dict[str,str]]) -> Dict[str,str]:
    for m in all_maps:
        keys = set()
        good = True
        for d in digits:
            n = get_mapped_digit(d, m)
            if n is None or n in keys:
                good = False
                break
            keys.add(n)
        if good:
            return m
    return None

def part1(displays: Tuple[List[str],List[str]]) -> None:
    signals_used = sum([sum([1 if len(x) in [2,3,4,7] else 0 for x in c]) for _,c in displays])
    print(signals_used)

def part2(displays: Tuple[List[str],List[str]]) -> None:
    
    all_maps = gen_all_maps()
    total = 0
    for digits,code in displays:
        m = get_correct_mapping(digits, all_maps)
        v = 0
        if m is not None:
            for c in code:
                v = v*10 + get_mapped_digit(c, m)
        total += v
    print(f'total: {total}')

# part1(data)
part2(data)

