#!/usr/bin/env python3
from functools import cmp_to_key
from json import loads
from typing import List,Tuple,AnyStr

data: List[Tuple[AnyStr]] = []

with open('./data.txt') as f:
    data = [x.split('\n') for x in f.read().strip().split('\n\n')]

def compare(L:List[any], R:List[any]) -> int:
    ordered = is_ordered_correctly(L,R)
    if ordered is None:
        return 0
    if ordered:
        return -1
    else:
        return 1
def is_ordered_correctly(_L:List[any], _R:List[any]) -> bool | None:
    L = _L[:]
    R = _R[:]
    # print(L,'<=>',R)
    ll = len(L)
    lr = len(R)
    if ll < lr:
        L += [None]*(lr-ll)
    elif lr < ll:
        R += [None]*(ll-lr)

    for l,r in zip(L,R):
        # if the left list runs out of items first, ordered
        if l is None:
            return True
        # if the right list runs out of items first, not ordered
        if r is None:
            return False

        tl = type(l)
        tr = type(r)
        # if they're both integers
        if tl == int and tr == int:
            # if the left integer is lower than the right, ordered
            if l < r: return True
            # if the left is highter than the right, not ordered
            elif l > r: return False
            #otherwise continue checking
        # if both values are lists
        elif tl == list and tr == list:

            ordered = is_ordered_correctly(l,r)
            if ordered is not None:
                return ordered
        elif tl == int and tr == list:
            l = [l]
            ordered = is_ordered_correctly(l,r)
            if ordered is not None:
                return ordered
        elif tr == int and tl == list:
            r = [r]
            
            ordered = is_ordered_correctly(l,r)
            if ordered is not None:
                return ordered
        else:
            raise f'unknown combination {tl} and {tr}'
    return None

def part1(d: List[Tuple[AnyStr]]):
    idx_sum = 0
    for i,(l,r) in enumerate(d):
        L = loads(l)
        R = loads(r)
        if is_ordered_correctly(L,R):
            # print(i+1)
            idx_sum += (i+1)
    print(f'sum of correctly ordered indices: {idx_sum}')

def part2(d: List[Tuple[AnyStr]]):
    two = [[2]]
    six = [[6]]

    pakets = [two,six]
    for pair in d:
        pakets += [loads(x) for x in pair]
    pakets.sort(key=cmp_to_key(compare))
    for p in pakets:
        print(p)
    two_idx = pakets.index(two)+1
    six_idx = pakets.index(six)+1
    
    print(f'decoder = {two_idx} * {six_idx} = {two_idx*six_idx}')

# part1(data)
part2(data)
