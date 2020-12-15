#!/usr/bin/env python3

data = []

with open('./data.txt') as f:
    data = [int(n) for n in f.readline().strip().split(',')]

# samples
# data = [0,3,6]
# data = [1,3,2]
# data = [2,1,3]
# data = [1,2,3]

def speak_next(nums):
    last_n = nums[0]
    next_n = nums[1:].index(last_n) + 1 if last_n in nums[1:] else 0
    return next_n

def part1(d):
    d.reverse()
    n = d[0]
    starting_count = len(d)

    for _ in range(starting_count, 2020):
        n = speak_next(d)
        d.insert(0, n)

    print(f'2020th number spoken: {n}')

def part2(d):
    # keys are spoken numbers
    # value is index of last speak
    db = {}
    
    #seed the db
    for pos,c in enumerate(d):
        db[c] = pos
    
    # remove the last seed number from db
    del db[d[-1]]
    
    # set the last seed number as the next to be spoken
    spoken = None
    to_speak = d[-1]

    for i in range(len(d)-1, 30000000):
        # speak the next number
        spoken = to_speak

        if i > (30000000 - 10):
            print(f'{spoken}')
        # find out if the spoken number has been spoken before
        # if not previously spoken, the next speak is 0
        # if yes previously spoken, the next speak is current position - last spoken position
        to_speak = 0 if spoken not in db else (i - db[spoken])
        
        # update the db for the spoken number and current position
        db[spoken] = i


    print(f'last spoken number: {spoken}')
# part1(data[:])
part2(data[:])

    
