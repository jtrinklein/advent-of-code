#!/usr/bin/env python3

from typing import List

data = []
with open('./data.txt') as f:
# with open('./test.txt') as f:
    data = [list(x.strip()) for x in f.readlines()]

def find_first_invalid(chunk: List[str]) -> str:
    openers = ['(', '[', '<', '{']
    pairs = {
        ']':'[',
        '>':'<',
        ')':'(',
        '}':'{',
        '[':']',
        '<':'>',
        '(':')',
        '{':'}',
    }
    expected_closer = []
    for c in chunk:
        if c in openers:
            expected_closer.append(pairs[c])
        else:
            
            if c != expected_closer[-1]:
                return c
            else:
                expected_closer.pop()
    return None

def get_autocomplete_score(chunk: List[str]) -> str:
    openers = ['(', '[', '<', '{']
    pairs = {
        ']':'[',
        '>':'<',
        ')':'(',
        '}':'{',
        '[':']',
        '<':'>',
        '(':')',
        '{':'}',
    }
    expected_closer = []
    for c in chunk:
        if c in openers:
            expected_closer.append(pairs[c])
        else:
            
            if c != expected_closer[-1]:
                return 0
            else:
                expected_closer.pop()
    points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }

    score = 0
    for c in reversed(expected_closer):
        score = score*5 + points[c]
    return score

def part1(d):
    
    invalid_points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
        None: 0
    }

    score = sum([invalid_points[find_first_invalid(chunk)] for chunk in d])
        
    print(f'score: {score}')

def part2(d):
    scores = [ get_autocomplete_score(chunk) for chunk in d ]
    scores = [x for x in scores if x != 0]
    scores.sort()
    middle = len(scores)//2
    score = scores[middle]
    print(f'autocomplete score: {score}')


part1(data)
part2(data)

