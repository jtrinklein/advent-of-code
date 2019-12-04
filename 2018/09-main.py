#!/usr/bin/env python3
from collections import deque

data_player_count = 470
data_last_marble_value = 72170

def play_game(players, last_marble_value):

    player_idx = 0
    # current_idx = 0
    scores = [0] * players
    # circle = [0]
    circle = deque([0])

    for m in range(1, last_marble_value + 1):
        
        if m % 23 == 0:
            
            # i = (current_idx - 7) % len(circle)
            # scores[player_idx] += circle.pop(i) + m
            # current_idx = i
            circle.rotate(7)
            scores[player_idx] += circle.pop() + m
            circle.rotate(-1)
        else:
            # csize = len(circle)
            # i = (current_idx + 1) % csize + 1
            # circle.insert(i, m)
            # current_idx = i
            circle.rotate(-1)
            circle.append(m)
            
        
        player_idx = (player_idx + 1) % players


    print(f'high score: {max(scores)}')

def part1():
    # 388024
    print('expect: 388024')
    play_game(data_player_count, data_last_marble_value)

def part2():
    # part 1 was solved with list and list manipulations
    # part 2 was taking forever so i looked up a solution :/
    print('expect: ???')
    play_game(data_player_count, data_last_marble_value*100)

def test():
    # 32
    print('expect: 32')
    play_game(9, 25)

test()
part1()
part2()