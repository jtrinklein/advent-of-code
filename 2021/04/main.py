#!/usr/bin/env python3
from functools import reduce

numbers = []
boards = []

with open('./data.txt') as f:
    data = [x.strip() for x in f.readlines()]
    numbers = [int(x) for x in data[0].split(',')]
    for line in data[1:]:
        if len(line) == 0:
            boards.append([])
        else:
            boards[-1].append([int(x) for x in line.strip().split(' ') if x])

def is_win(stamps):
    and_all = lambda a,b: a and b
    for i,s in enumerate(stamps):

        if reduce(and_all, s):
            return True
        if reduce(and_all, [x[i] for x in stamps]):
            return True
    return False
def print_stamps(stamps):
    print('------')
    for s in stamps:
        print(' '.join(['x' if v else 'o' for v in s]))
    print('------')
    
def print_board(board):
    print('======')
    for b in board:
        print(' '.join([str(B) for B in b]))
    print('======')

def check_board(nums, board, count_limit):
    stamps = []
    for l in board:
        stamps.append([False for _ in l])

    for i, n in enumerate(nums):
        if (i+1) > count_limit:
            return count_limit, None

        for j, line in enumerate(board):
            if n in line:
                idx = line.index(n)
                stamps[j][idx] = True
                
                if is_win(stamps):
                    s = 0
                    for k,v in enumerate(stamps):
                        s += sum([vv if not v[kk] else 0 for kk,vv in enumerate(board[k])])
                    
                    # print_stamps(stamps)
                    # print_board(board)
                    return i+1, s*n
                    
                


def part1(numbers, boards):
    best_count = len(numbers)
    best_score = 0
    for b in boards:
        # print('><><><><><><><')
        # print_board(b)
        c, score = check_board(numbers, b, best_count)
        print(f'board got score {score} in {c} nums')
        if score:
            if c < best_count:
                best_score = score
                best_count = c
            elif c == best_count and score > best_score:
                best_score = score

    print(f"best score {best_score} in {best_count} numbers")

def part2(numbers, boards):
    nums_count = len(numbers)
    longest_count = 0
    best_score = 0
    for b in boards:
        c, score = check_board(numbers, b, nums_count)
        print(f'board got score {score} in {c} nums')
        if score:
            if c > longest_count:
                best_score = score
                longest_count = c
            elif c == longest_count and score > best_score:
                best_score = score

    print(f"best score {best_score} in {longest_count} numbers")


# test_nums = [1,2,8,4,7,3,5]
# test_boards = [
#     [
#         [1,2,8],
#         [0,0,0],
#         [0,0,5]
#     ],
#     [
#         [1,0,0],
#         [2,0,0],
#         [8,0,7]
#     ],
#     [
#         [1,0,0],
#         [2,0,0],
#         [4,0,6]
#     ]
# ]

# part1(numbers, boards)
part2(numbers, boards)