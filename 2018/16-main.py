#!/usr/bin/env python3

samples = None
with open('./16-data.txt') as f:
    samples = f.read().splitlines()

program = None
with open('./16-program.txt') as f:
    program = f.read().splitlines()

opNames = [
    'addr',
    'addi',
    'mulr',
    'muli',
    'banr',
    'bani',
    'borr',
    'bori',
    'setr',
    'seti',
    'gtir',
    'gtri',
    'gtrr',
    'eqir',
    'eqri',
    'eqrr'
]

stats = {
    'addr': {},
    'addi': {},
    'mulr': {},
    'muli': {},
    'banr': {},
    'bani': {},
    'borr': {},
    'bori': {},
    'setr': {},
    'seti': {},
    'gtir': {},
    'gtri': {},
    'gtrr': {},
    'eqir': {},
    'eqri': {},
    'eqrr': {},
    'multiop': 0
}

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
optest = {
    'addr': lambda a,b,reg,val: val == opexec['addr'](a,b,reg), # adding register A and register B
    'addi': lambda a,b,reg,val: val == opexec['addi'](a,b,reg),      # adding register A and value B
    'mulr': lambda a,b,reg,val: val == opexec['mulr'](a,b,reg),
    'muli': lambda a,b,reg,val: val == opexec['muli'](a,b,reg),
    'banr': lambda a,b,reg,val: val == opexec['banr'](a,b,reg),
    'bani': lambda a,b,reg,val: val == opexec['bani'](a,b,reg),
    'borr': lambda a,b,reg,val: val == opexec['borr'](a,b,reg),
    'bori': lambda a,b,reg,val: val == opexec['bori'](a,b,reg),
    'setr': lambda a,b,reg,val: val == opexec['setr'](a,b,reg),
    'seti': lambda a,b,reg,val: val == opexec['seti'](a,b,reg),
    'gtir': lambda a,b,reg,val: val == opexec['gtir'](a,b,reg),
    'gtri': lambda a,b,reg,val: val == opexec['gtri'](a,b,reg),
    'gtrr': lambda a,b,reg,val: val == opexec['gtrr'](a,b,reg),
    'eqir': lambda a,b,reg,val: val == opexec['eqir'](a,b,reg),
    'eqri': lambda a,b,reg,val: val == opexec['eqri'](a,b,reg),
    'eqrr': lambda a,b,reg,val: val == opexec['eqrr'](a,b,reg)
}

# this was added to as each one was determined
known = {
    '0':'eqri',
    '1':'bani',
    '2':'seti',
    '3':'bori',
    '4':'eqir',
    '5':'banr',
    '6':'borr',
    '7':'muli',
    '8':'setr',
    '9':'addr',
    '10':'eqrr',
    '11':'addi',
    '12':'gtir',
    '13':'gtrr',
    '14':'gtri',
    '15':'mulr',
}
multi = 0
def test_sample(before, after, instruction):
    global stats
    global multi
    # The output, C, is always treated as a register
    op, a, b, c = instruction
    op = str(op)
    val = after[c]
    if op in known:
        opname = known[op]
        stats[opname][op] = stats[opname].get(op,0) +1
        stats[op][opname] = stats[op].get(opname,0) +1
        return 
    matches = 0
    for opname in opNames:
        r = optest[opname](a,b,before,val)
        # print('testing', op, ':', opname, '->', r)
        if r:
            stats[opname][op] = stats[opname].get(op,0) +1
            stats[op][opname] = stats[op].get(opname,0) +1
            
            matches += 1
    
    if matches > 2:
        # stats['multiop'] = stats.get('multiop', 0) + 1
        multi += 1


# test_sample([0, 1, 2, 1], [0, 1, 1, 1], [12, 3, 2, 2])
# print(stats)
samplecount = 0
for i in range(16):
    stats[str(i)] = {}

while len(samples) > 0:
    samplecount += 1
    
    before = [int(x) for x in samples.pop(0).split('[')[1][:-1].split(', ')]
    ins    = [int(x) for x in samples.pop(0).split()]
    after  = [int(x) for x in samples.pop(0).split('[')[1][:-1].split(', ')]
    
    samples.pop(0) #empty line
    test_sample(before,after, ins)

# for name in opNames:
#     count = -1
#     op = -1
    
#     for i in range(16):
#         n = stats[name].get(str(i), 0)
#         if n > count:
#             op = i
#             count = n
#     print(f"'{op}':'{name}',")

print('-------------------')
for i in range(16):
    count = -1
    opname = None
    if str(i) in known:
        opname = known[str(i)]
        # print(f"'{i}':'{opname}', KNOWN\n" )

    else:
        for name in opNames:
            n = stats[str(i)].get(name, 0)
            if name in known.values():
                continue
            else:
                print(f"{name}:=> {n}")
            if n > count:
                opname = name
                count = n
        # print(stats[str(i)])
        # print(f"'{i}':'{opname}',\n")

print('multiop:', stats['multiop'])
print('multiop:', multi)
print('samples:', samplecount)
print('lines:', samplecount*4)

regs = [0,0,0,0]
for p in program:
    op, a, b, c = [int(x) for x in p.split()]
    regs[c] = opexec[known[str(op)]](a,b,regs)

print(regs)

