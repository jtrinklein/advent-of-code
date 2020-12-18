#!/usr/bin/env python3

data = []

with open('./data.txt') as f:
    data = [line.strip() for line in f.readlines()]

def eval_expr(ex):
    # a is always a literal
    # op is one of +,*,)
    # b is either a literal or (
    # evaluate a op b for s = n*m or s = n+m and return [s] + expressionlist
    # ex: 1+2+3
    # ex   = [1,+,2,+,3]
    # a = 1, op = 2, b = 3
    # return [    3,+,3]

    while len(ex) > 1:

        # may only have 2 left if ex ends with closing parens
        if ex[1] == ')':
            return ex[0:1] + ex[2:]

        a,op,b = ex[0:3]
        # nested parens can lead to a being (
        # ex 1 + ((2 * 3) * 4)
        if a == '(':
            ex = eval_expr(ex[1:])
        elif b == '(':
            ex = [a,op] + eval_expr(ex[3:])
        elif op == '+':
            ex = [a+b] + ex[3:]
        elif op == '*':
            ex = [a*b] + ex[3:]
    return ex

def process_input(s):
    return [int(x) if x.isnumeric() else x for x in list(s.strip().replace(' ', ''))]

def part1(d):
    total = 0
    for line in d:
        expr = process_input(line)
        answer = eval_expr(expr)[0]
        total += answer
        print(answer)
    print(f'sum of all expressions is {total}')

# data =  [
#     '2 * 3 + (4 * 5)',
#     # = 26
#     '5 + (8 * 3 + 9 + 3 * 4 * 3)',
#     # = 437
#     '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))',
#     #= 12240
#     '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2',
#     #= 13632.
# ]

part1(data)