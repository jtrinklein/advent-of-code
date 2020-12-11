#!/usr/bin/env python3
data = []

with open('./data.txt') as f:
    data = [int(line) for line in f.readlines()]

def get_diffs(d):
    '''
    gets the voltage difference between adjacent adapters
    example:
    given the adapters: 1, 4, 7, 8
    add the wall as starting at 0: (0), 1, 4, 7, 8
    generate a list of (adapter[i+1] - adapter[i])
    difference list: [1,3,3,1]
    add the device as a +3 difference at the end
    final list: [1,3,3,1,3]
    '''
    d.sort()
    # wall joltage starts at 0
    d = [0] + d 
    diffs = [y-x for x,y in zip(d[:-1], d[1:])] + [3] # device is guaranteed to be +3 from last adapter
    return diffs

def part1(d):
    diffs = get_diffs(d)

    ones = diffs.count(1)
    threes = diffs.count(3)

    print(f'{ones} +1 diffs, {threes} +3 diffs = {ones * threes}')


#======== I will always figure out the recursive attempt first :D
def find_next_removal_point(diffs):
    for i in range(len(diffs) -1):
        if diffs[i] + diffs[i+1] <= 3:
            yield i


def count_configurations(diffs):
    count = 1
    for i in range(len(diffs)):
        sub_diffs = diffs[i:]
        for remove_index in find_next_removal_point(sub_diffs):
            rval = sub_diffs[remove_index]
            more_diffs = sub_diffs[remove_index+1:]
            more_diffs[0] += rval
            count += count_configurations(more_diffs)
    return count
#================================================================

def get_tribonacci_number(n): 
    '''
    function to generate tribonacci numbers
    taken from: https://www.geeksforgeeks.org/tribonacci-numbers/
    '''

    #seed the algorithm
    x = [0] * (n+3)
    x[0] = 0
    x[1] = 0
    x[2] = 1

    for i in range(3,n+3):
        x[i] = x[i - 1] + x[i - 2] + x[i - 3]
    return x[-1]

def get_estimate(diffs):
    '''
    take the list of diffs and:
    - join them in a string
    - replace 13 with 1,
    - remove all other 3s
    - split into a list at ,
    - make each entry the length of the string ex: ['1111','11'] -> [4,2]

    using that list
    - find the max group length
    - for group lengths from 2 to max : (l)
       - get the tribonacci number for the group length (t)
       - get the number of groups with length l : (c)
       keep a running product of (t) raised to the power of (c)
    '''
    regions = [len(x) for x in ''.join([str(x) for x in diffs]).replace('13', '1,').replace('3', '').split(',')]
    total = 1

    for i in range(2, max(regions)+1):
        t = get_tribonacci_number(i)
        c = regions.count(i)
        total *= t**c

    return total

def part2(d):
    diffs = get_diffs(d)
    print(f'1s: {diffs.count(1)}')
    print(f'2s: {diffs.count(2)}')
    print(f'3s: {diffs.count(3)}')
    print(f'estimate: {get_estimate(diffs)}')

sample1 = [1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19]
sample2 = [1,  2,  3,  4,  7,  8,  9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31, 32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 48, 49]

print('part1:')
part1(data)
print('================\npart2:')
print('sample1: should be 8')
part2(sample1)
print('-------\nsample2: should be 19208')
part2(sample2)
print('-------\ndata: ???')
part2(data)
'''
Trying to manually work out a mathy solution with sample 1 data
(0), 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, (22)
   1, 3, 1, 1, 1, 3,  1,  1,  3,  1,  3,  3
   F  F  O  O  F  F   O   F   F   F   F   
         \  /         |
           2  +       1 = 3
            2^3 = 8   
   3 OPEN (not fixed) points
   8 arrangements
    works!
'''

'''
trying to manually work out sample 2 data
(0),  1,  2,  3,  4,  7,  8,  9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31, 32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 48, 49, (52)
    1,  1,  1,  1,  3,  1,  1,  1,  1,  3,  3,  1,  1,  1,  3,  1,  1,  3,  3,  1,  1,  1,  1,  3,  1,  3,  3,  1,  1,  1,  1,  3
    O   O   O   F   F   O   O   O   F   F   F   O   O   F   F   O   F   F   F   O   O   O   F   F   F   F   F   O   O   O   F
        3                   3                     2             1                   3                               3
        3 + 3  + 2 + 1  + 3 + 3 = 15
        2 ^ 15 = 32768

    14 OPEN (not fixed) points
    19208 arrangements
    doesn't work, need some other kind of math....
'''