#!/usr/bin/env python3


start = 197487
end = 673251

# start = 0
# end = 999999
# 
def is_valid_code(n, part2=False, debug=False):
    sn = str(n)
    # It is a six-digit number.
    if len(sn) != 6:
        if debug:
            print('failed digit count')
        return False
    # The value is within the range given in your puzzle input.
    if n < start or n > end:
        if debug:
            print('failed bounds check')
        return False
    # Two adjacent digits are the same (like 22 in 122345).
    repeat = False
    d = []
    for i in range(len(sn)-1):
        if sn[i] == sn[i+1]:
            repeat = True
            if not sn[i] in d:
                d.append(sn[i])
    if not repeat:
        if debug:
            print('failed repeat')
        return False

    if part2:
        # the two adjacent matching digits are not part of a larger group of matching digits
        one_double = False
        for i in d:
            if not one_double and list(sn).count(i) == 2:
                one_double = True
        
        if not one_double:
            if debug:
                print('failed group of only 2 digits')
            return False

    # Going from left to right, the digits never decrease;
    #  they only ever increase or stay the same (like 111123 or 135679).
    for i in range(len(sn)-1):
        if int(sn[i]) > int(sn[i+1]):
            if debug:
                print('failed increasing digits')
            return False
    return True

def part1():
    count = 0
    for c in range(start, end):
        if is_valid_code(c):
            count += 1

    print(f'number of valid codes: {count}')

def part2():
    count = 0
    for c in range(start, end):
        if is_valid_code(c, part2=True):
            count += 1

    print(f'number of valid codes: {count}')

# part1()
part2()