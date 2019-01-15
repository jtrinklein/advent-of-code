#!/usr/bin/env python3

data = None
with open('./19-data.txt') as f:
    data = f.read().splitlines()

# data = [
#     '#ip 0',
#     'seti 5 0 1',
#     'seti 6 0 2',
#     'addi 0 1 0',
#     'addr 1 2 3',
#     'setr 1 0 0',
#     'seti 8 0 4',
#     'seti 9 0 5',
# ]

    
  
    




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


def the_program(part2=False):
    r0 = 1 if part2 else 0 # part 2 r0 = 1, part1 r0 = 0
    r2 = 0
    r3 = 0

    ## instructions start here
    r2 += 2
    r2 *= r2
    r2 *= 19
    r2 *= 11
    r3 += 6
    r3 *= 22
    r3 += 8
    r2 += r3

    if r0 == 1:
        r3 = 27
        r3 *= 28
        r3 += 29
        r3 *= 30
        r3 *= 14
        r3 *= 32
        r2 += r3
        r0 = 0
    s = 0
    for i in range(1, r2+1):
        # // is floor division 3//2 is 1 where 3/2 is 1.5
        # but 2/1 is 2 and a proper integer so 2/1 == 2//1
        if r2 // i == r2 / i:
            s += i
    print('the final answer:', s)

register_count = 6
reg = [0 for x in range(register_count)]
# #ip 4
ipreg = int(data.pop(0).split()[-1])

program = []
for line in data:
    #addi 4 16 4
    parts = line.split()
    ins = parts.pop(0)
    a,b,c = [ int(x) for x in parts ]
    program.append([ins, a, b, c])

def run(program, ipstart=0, r5sumstart=0, debug=False):
    cycles = 0
    if debug:
        print(reg, cycles)
    ip = ipstart
    r0last = reg[0]
    r5sum = r5sumstart
    rout = ''
    runner = 0
    while ip >= 0 and ip < len(program):
        cycles += 1
        # if cycles%1000000 == 0:
        #     print(cycles, ip, reg)
        # put ip in ipreg
        reg[ipreg] = ip
        if debug:
            
            rout = str(reg)

        # if debug:
        #     print(f"ip: {ip}, reg: {reg}")
        
        # run instruction
        # if debug:
        #     print(program[ip])
        ins,a,b,c = program[ip]
        reg[c] = opexec[ins](a,b,reg)
        if debug:
            if ip == 7:
                print(reg)
            if runner == 0:
                print(ins, a, b, c, '  ', rout, '->', reg, '->', reg[ipreg]+1)
                ipt = input()
                if ipt == 'x':
                    return
                try:
                    runner = int(ipt)
                except:
                    runner = 0
            else:
                runner -= 1
        elif r0last != reg[0]:
            print(r0last, reg)
            if reg[1] > reg[5]:
                reg[0] = r0last + r5sum
                return

            r5sum += reg[5]
            r0last = reg[0]
        
        # pull ip from ipreg
        ip = reg[ipreg] + 1
        # print(reg[0], ip, reg)


def part1_run():
    for i in range(len(reg)):
        reg[i] = 0
        
    run(program, debug=False)
    print('What value is left in register 0 when the background process halts?')
    print(f"reg[0]: {reg[0]}")

def part2_run():
    global reg
    for i in range(len(reg)):
        reg[i] = 0
    reg[0] = 1
    # reg = [64, 22, 10551376, 1, 7, 479608]
    # reg = [42, 16, 10551376, 1, 7, 659461]
    run(program,debug=True)
    print('What value is left in register 0 when the background process halts?')
    print(f"reg[0]: {reg[0]}")

def part1():
    the_program()

def part2():
    the_program(part2=True)

# part1()
part2()