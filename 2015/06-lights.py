#!/usr/local/bin/python3

data = None
with open('./06-data.txt') as f:
    data = f.read()

data = data.splitlines()

lights = {}
def get_index(x, y):
    return f"{x}|{y}"

def get_value(x, y):
    i = get_index(x, y)
    if i in lights:
        return lights[i]
    
    return 0

def set_value(x, y, v):
    i = get_index(x, y)
    lights[i] = v

def light_toggle(x, y):
    v = get_value(x,y)
    set_value(x, y, v + 2)

def light_on(x,y):
    v = get_value(x, y)
    set_value(x, y, v + 1)
    

def light_off(x,y):
    v = get_value(x, y)
    if v > 0:
        v = v - 1
    set_value(x, y, v)

def range_toggle(x0,y0, x1, y1):
    [light_toggle(x, y) for x in range(x0, x1+1) for y in range(y0, y1+1)]

def range_on(x0,y0, x1, y1):
    [light_on(x, y) for x in range(x0, x1+1) for y in range(y0, y1+1)]

def range_off(x0,y0, x1, y1):
    [light_off(x, y) for x in range(x0, x1+1) for y in range(y0, y1+1)]

def parse_instruction(str):
    ins = str[:]
    cmd = None
    if ins.startswith('turn on'):
        cmd = 'on'
        ins = ins[len('turn on '):]
    elif ins.startswith('turn off'):
        cmd = 'off'
        ins = ins[len('turn off '):]
    elif ins.startswith('toggle'):
        cmd = 'toggle'
        ins = ins[len('toggle '):]

    start, end = [[int(y) for y in x.split(',')] for x in ins.split(' through ')]

    return [cmd] + start + end

def execute_instruction(ins):
    cmd, x0,y0,x1,y1 = ins
    if cmd is 'on':
        range_on(x0,y0,x1,y1)

    elif cmd is 'off':
        range_off(x0,y0,x1,y1)

    elif cmd is 'toggle':
        range_toggle(x0,y0,x1,y1)
    else:
        raise f'Unknown Instruction: {cmd}'

for cmd in data:
    ins = parse_instruction(cmd)
    execute_instruction(ins)

lit = sum([v for k,v in lights.items()])

print(f'lights value: {lit}')
