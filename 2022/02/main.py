#!/usr/bin/env python3

R = 'Rock'
P = 'Paper'
S = 'Scissors'

W = 'win'
T = 'tie'
L = 'lose'

values = {
    R: 1,
    P: 2,
    S: 3,
}
def is_win(o: str,m: str) -> bool : 
    return (
        (m == R and o == S) or
        (m == S and o == P) or
        (m == P and o == R)
    )

data = []
with open('./data.txt') as f:
    data = [x.strip().split(' ') for x in f.readlines()]

def get_my_score(round_info) -> int:
    theirs,mine,win = round_info
    if win:
        return mine + 6
    elif mine == theirs:
        return mine + 3
    return mine

def part1(d):
    choices = {
        'A': R,
        'B': P,
        'C': S,
        'X': R,
        'Y': P,
        'Z': S,
    }
    tmp = [[choices[y] for y in x] for x in d]
    rounds = [[values[y] for y in x] + [is_win(x[0], x[1])] for x in tmp]
    final_score = sum([get_my_score(x) for x in rounds])
    print(f'Final score: {final_score}')

def get_win(move) -> str:
    if move == R:
        return P
    elif move == P:
        return S
    return R

def get_loss(move) -> str:
    if move == R:
        return S
    elif move == P:
        return R
    return P

def get_my_move(theirs, result) -> str:
    if result == W:
        return get_win(theirs)
    elif result == L:
        return get_loss(theirs)
    return theirs

def part2(d):    
    instructions = {
        'A': R,
        'B': P,
        'C': S,
        'X': L,
        'Y': T,
        'Z': W,
    }
    tmp = [[instructions[y] for y in x] for x in d]
    
    rounds = [[values[x[0]], values[get_my_move(x[0], x[1])], x[1] == W] for x in tmp]
    final_score = sum([get_my_score(x) for x in rounds])
    print(f'Final score part 2: {final_score}')

#part1(data)
part2(data)