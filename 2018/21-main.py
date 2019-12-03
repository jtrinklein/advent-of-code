#!/usr/bin/env python3

data = None
with open('./21-data.txt') as f:
    data = f.read().splitlines()

opexec = {
    'addr': lambda a,b,reg: (reg[a] + reg[b]), # adding register A and register B
    'addi': lambda a,b,reg: (reg[a] + b),      # adding register A and value B
    'mulr': lambda a,b,reg: (reg[a] * reg[b]), # multiplying register A and register B
    'muli': lambda a,b,reg: (reg[a] * b),      # multiplying register A and value B
    'banr': lambda a,b,reg: (reg[a] & reg[b]), # bitwise AND of register A and register B
    'bani': lambda a,b,reg: (reg[a] & b),      # bitwise AND of register A and value B
    'borr': lambda a,b,reg: (reg[a] | reg[b]), # bitwise OR of register A and register B
    'bori': lambda a,b,reg: (reg[a] | b),      # bitwise OR of register A and value B
    'setr': lambda a,b,reg: reg[a],            # register A into register C
    'seti': lambda a,b,reg: a,                 # value A into register C
    'gtir': lambda a,b,reg: int(a > reg[b]),   # value A is greater than register B
    'gtri': lambda a,b,reg: int(reg[a] > b),   # register A is greater than value B
    'gtrr': lambda a,b,reg: int(reg[a] > reg[b]), # register A is greater than register B
    'eqir': lambda a,b,reg: int(a == reg[b]), # value A is equal to register B
    'eqri': lambda a,b,reg: int(reg[a] == b), # register A is equal to value B
    'eqrr': lambda a,b,reg: int(reg[a] == reg[b]) # register A is equal to register B
}


def secret_prog(r0_initial=0, part1=False):
    r0 = r0_initial
    r1 = 0
    r2 = 0
    r4 = 0
    r5 = 0

    while r5 != 72:
        r5 = 123
        r5 = r5 & 456
    r5 = 0
    r4 = r5 | 65536
    r5 = 8858047
    cycles = 7
    solutions = []
    found_part1 = False
    while True:
        r2 = r4 & 255
        r5 = r2 + r5
        
        # keep only the lower 24 bits of r5
        r5 = r5 & 16777215
        r5 = r5 * 65899
        # keep lower 24 bits of r5
        r5 = r5 & 16777215
        cycles += 5
        if r4 < 256:
            
            # not part of original program, its the solver --V
            if r5 not in solutions:
                if not found_part1:
                    print(f'part1: smallest value that finishes with minimal cycles: {r5}')
                    found_part1 = True
                solutions.append(r5)
            else:
                print(f'part2: smallest value that finishes with most cycles: {r5}')
                return cycles + 5                
                # return cycles
            # -----------------------------------------------^

            if r5 == r0:
                cycles += 5
                return cycles
            else:
                r4 = r5 | 65536
                r5 = 8858047
                cycles += 8
                continue
        else:
            r2 = 0
            cycles += 4

        while True:
            # print([r0,r1,r2,r3,r4,r5])
            # if input() == 'x':
            #     return
            r1 = r2 + 1
            r1 = r1 * 256
            cycles += 2

            if r1 > r4:
                r4 = r2
                cycles += 5
                break
            else:
                r2 += 1
                cycles += 5
        



# run_prog(program, 11513432)
secret_prog()


# Reverse engineered program:

# ipreg= 3
#  0: seti 123 0 5
#     123 -> r5

#  1: bani 5 456 5
#     r5 & 456 -> r5
#     r5 = r5 & 456

#  2: eqri 5 72 5
#     r5 == 72 -> r5

#  3: addr 5 3 3
#     r5 + r3 -> r3
#     r5 + 3 -> r3
#     if r5 == 72:
#         # 1 + 3 -> r3  # ni = 5
#         GOTO 5
#     else:
#         # 0 + 3 -> r3  # ni = 4
#         GOTO 4
    
#  4: seti 0 0 3
#     # 0 -> r3  # ni = 1
#     GOTO 1

# # main program
#  5: seti 0 3 5
#     0 -> r5
#     r5 = 0

#  6: bori 5 65536 4
#     r5 | 65536 -> r4
#     check bit 16: r5 | b1 0000 0000 0000 0000
#     r4 = r5 | 65536
 
#  7: seti 8858047 4 5
#     8858047 -> r5
#     r5 = 8858047
 
#  8: bani 4 255 2
#     r4 & 255 -> r2
#     grab the lower 8 bits of r4
#     r2 = r4 & 255
 
#  9: addr 5 2 5
#     r5 + r2 -> r5
#     r5 = r2 + r5

# 10: bani 5 16777215 5
#     r5 & 16777215 -> r5
#     keep only the lower 24 bits of r5
#     r5 = r5 & 16777215

# 11: muli 5 65899 5
#     r5 * 65899 -> r5
#     r5 = r5 * 65899

# 12: bani 5 16777215 5
#     r5 & 16777215 -> r5
#     keep lower 24 bits of r5
#     r5 = r5 & 16777215

# 13: gtir 256 4 2
#     256 > r4 -> r2
#     if r4 < 256:

# 14: addr 2 3 3
#     r2 + r3 -> r3
#     if r4 < 256:
#         1 + r3 -> r3
#         1 + 14 -> r3 # ni -> 16
#         GOTO 16    
#         # GOTO 28
#     else:
#         0 + r3 -> r3
#         0 + 14 -> r3 # ni -> 15
#         GOTO 15
#         # GOTO 17

# 15: addi 3 1 3
#     r3 + 1 -> r3
#     15 + 1 -> r3 # ni -> 17
#     GOTO 17

# 16: seti 27 5 3
#     27 -> r3
#     GOTO 28

# 17: seti 0 6 2
#     0 -> r2
#     r2 = 0
# 18: addi 2 1 1
#     r2 + 1 -> r1
#     r1 = r2 + 1

# 19: muli 1 256 1
#     r1 * 256 -> r1
#     r1 = r1 * 256

# 20: gtrr 1 4 1
#     r1 > r4 -> r1
#     if r1 > r4:

# 21: addr 1 3 3
#     r1 + r3 -> r3
#     r1 + 21 -> r3
#     if r1 > r4:
#         1 + 21 -> r3  # ni -> 23
#         GOTO 23
#         # GOTO 26
#     else:
#         0 + 21 -> r3  # ni -> 22
#         GOTO 22
#         # GOTO 24

# 22: addi 3 1 3
#     r3 + 1 -> r3
#     22 + 1 -> r3  # ni -> 24
#     GOTO 24

# 23: seti 25 1 3
#     25 -> r3  # ni -> 26
#     GOTO 26

# 24: addi 2 1 2
#     r2 + 1 -> r2
#     r2 += 1

# 25: seti 17 4 3
#     17 -> r3  # ni -> 18
#     GOTO 18

# 26: setr 2 1 4
#     r2 -> r4
#     r4 = r2

# 27: seti 7 3 3
#     7 -> r3  # ni -> 8
#     GOTO 8

# 28: eqrr 5 0 2
#     r5 == r0 -> r2

# 29: addr 2 3 3
#     r2 + r3 -> r3
#     r2 + 29 -> r3
#     if r0 == r5:
#         1 + 29 -> r3  # ni -> 31 
#         EXIT
#     else:
#         GOTO 6

# 30: seti 5 2 3
#     5 -> r3  # ni -> 6
#     GOTO 6