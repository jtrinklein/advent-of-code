#!/usr/bin/env python3

data = []

with open('./data.txt') as f:
    data = [line.strip() for line in f.readlines()]


def update_mask(bits):
    set_mask = clear_mask = 0
    offset = len(bits)-1
    for i,b in enumerate(bits):
        if b == '1':
            set_mask |= 1 << (offset - i)
        elif b == '0':
            clear_mask |= 1 << (offset - i)
    return set_mask, clear_mask

def store_value(value, addr, mem, set_mask, clear_mask):
    mem[addr] = (int(value) & ~clear_mask) | set_mask

def run_program(instructions):
    set_mask = clear_mask = 0
    mem = {}
    for line in instructions:

        addr, value = line.split(' = ')
        # mask = X01X1XX01011X00110XX011100000111X01X
        if addr.startswith('mask'):
            set_mask, clear_mask = update_mask(value)

        # mem[20234] = 1730
        else:
            # dont need to get the number out of addr, its a unique key
            store_value(value, addr, mem, set_mask, clear_mask)
    return sum(mem.values())



def part1(d):
    value = run_program(d)
    print(f'final value: {value}')

def run_program_2(instructions):
    set_mask = clear_mask = 0
    variable_mask = None
    mem = {}
    for line in instructions:

        addr, value = line.split(' = ')
        # mask = X01X1XX01011X00110XX011100000111X01X
        if addr.startswith('mask'):
            set_mask = int(''.join([x if x == '1' else '0' for x in value ]), 2)
            # for this its more important where the x's fall in the mask
            # this gives us positions for changing the address
            # we can generate the different combinations by using the length of the list
            # ex: 4 x in the mask means 2^4 or 16 combinations: 0000, 0001, 0010
            # we can move each bit in those combinations to the correct place in the mask
            # by keeping track of where the x is located in the mask
            variable_mask = [i for i, x in enumerate(value) if x == 'X']
            clear_mask = int(value.replace('1','0').replace('X','1'), 2)

        else:
            # mem[20234] = 1730
            value = int(value)

            # actually need the number now
            addr = int(addr[4:-1])
            # now we need to update the address by the fixed ones in the mask
            addr |= set_mask
            # clear out all the positions that will be changed by the variable mask
            addr &= ~clear_mask

            # for the X masking we need to generate a unique mask for each of the combinations
            v_count = len(variable_mask)
            combo_count = 2 ** v_count
            for i in range(combo_count):
                # bin() adds 0b to the beginning, strip that with [2:]
                # zfill() adds 0 to the left of the string until it reaches the provided length
                minivmask = [int(x) for x in bin(i)[2:].zfill(v_count)]
                vmask = [0]*36
                # set the positions in the vmask according to the current combination
                for i,v in enumerate(minivmask):
                    vmask[variable_mask[i]] = v
                vmask = int(''.join([str(x) for x in vmask]), 2)
                # update the address and write the value
                mem[addr|vmask] = value
            
    return sum(mem.values())

def part2(d):
    value = run_program_2(d)
    print(f'final value: {value}')

#part1(data)
part2(data)

# m = max([x.count('X') for x in data])
# print(f'max X in a mask: {m}')
# max x in line is 9 - should not explode computer to bruteforce
part2(data)