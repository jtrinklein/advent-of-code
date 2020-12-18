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

def eval_different(ex):
    # first check for parentheticals
    while '(' in ex:
        pcount = 1
        start = ex.index('(')
        end = start
        #find the end of this parenthetical
        while pcount:
            end += 1
            if ex[end] == ')':
                pcount -=1
            elif ex[end] == '(':
                pcount += 1

        # evaluate the parenthetical
        v = eval_different(ex[start+1:end])
        # remove the parenthetical from the expression
        # and replace it with the value
        ex = ex[:start] + v + ex[end+1:]

    # no parentheticals, check for +
    # for all + operators in the expression
    while '+' in ex:
        i = ex.index('+')
        # evaluate the expression
        v = ex[i-1] + ex[i+1]
        # replace the expression with the value
        ex = ex[:i-1] + [v] + ex[i+2:]

    # no parentheticals or +, check for *
    # for all * operators in the expression
    while '*' in ex:
        i = ex.index('*')

        # evaluate the expression
        v = ex[i-1] * ex[i+1]
        # replace the expression with the value
        ex = ex[:i-1] + [v] + ex[i+2:]

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

def part2(d):
    total = 0 
    for line in d:
        expr = process_input(line)
        answer = eval_different(expr)[0]
        total += answer
    print(f'sum of all expressions using eval_different is {total}')

part2(data)
