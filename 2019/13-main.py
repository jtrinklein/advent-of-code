#!/usr/bin/env python3
import time
import pygame
# import platform
# if platform.system() == 'Windows':
#     from msvcrt import getch
# else:
#     #requires: pip install getch
#     from getch import getch

data = []

with open('./13-data.txt') as f:
    data = [int(x) for x in f.read().split(',')]

maxx = 45
maxy = 23
scale = 20
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 
black = (0, 0, 0)
red = (255, 0, 0)

pygame.init()
disp = pygame.display.set_mode((maxx*scale,maxy*scale))
pygame.display.set_caption('Drawing')
disp.fill(black)
time.sleep(5)
position_mode = 0
immediate_mode = 1
relative_mode = 2

empty = 0
wall = 1
block = 2
paddle = 3
ball = 4

vx_ball = 1
vy_ball = 1
cx_ball = None
cy_ball = 0
lastx_ball = None
lasty_ball = None
lastx_paddle = None
lasty_paddle = None
py = 0
bi = 0
grid = []
for y in range(maxy):
    grid.append([])
    for x in range(maxx):
        grid[-1].append(0)
def update_window():
    disp.fill(black) 
    for y in range(maxy):
        for x in range(maxx):
            v = grid[y][x]
            if v == ball:
                pygame.draw.circle(disp, red, (x*scale+(scale//2), y*scale+(scale//2)), (scale//2), 0) 
            elif v == wall:
                pygame.draw.rect(disp, blue, (x*scale, y*scale, scale, scale)) 
            elif v == paddle:
                pygame.draw.rect(disp, white, (x*scale, y*scale+(scale//2), scale, (scale//2))) 
            elif v == block:
                pygame.draw.rect(disp, green, (x*scale, y*scale, scale, scale)) 
                

def get_parameter_modes(op):
    """
     0 == position mode
     1 == immediate mode
     2 == relative mode
    """
    # the first parameter's mode is in the hundreds digit,
    mode1 = (op // 100) % 10
    # the second parameter's mode is in the thousands digit,
    mode2 = (op // 1000) % 10
    # the third parameter's mode is in the ten-thousands digit,
    mode3 = (op // 10000) % 10
    # and so on. 
    return [mode1, mode2, mode3]

def get_param_value(d, val, mode, rbase):
    if mode == immediate_mode:
        return val
    if mode == position_mode:
        return d[val]
    if mode == relative_mode:
        return d[rbase + val]
    raise 'Bad parameter mode'

def get_write_address(val, mode, rbase):
    if mode == relative_mode:
        return rbase + val
    return val

def id(x,y):
    return f'{x},{y}'

def write_obj(data, screen):
    x,y,d = data
    global grid
    global cx_ball
    global vx_ball
    global lastx_ball
    global cy_ball
    global vy_ball
    global lasty_ball
    global lastx_paddle
    global lasty_paddle
    grid[y][x] = d
    
    if d == ball:
        if cx_ball is None:
            cx_ball = x-1
            cy_ball = y-1
        lastx_ball = cx_ball
        lasty_ball = cy_ball
        cx_ball = x
        vx_ball = x-lastx_ball
        cy_ball = y
        vy_ball = y-lasty_ball
    elif d == paddle:
        lastx_paddle = x
        lasty_paddle = y
    screen[id(x,y)] = d

def printscreen(screen):
    for y in range(maxy):
        l = ''
        for x in range(maxx):
            i = id(x,y)
            v = screen.get(i, empty)
            if   v ==  empty: l += ' '
            elif v == paddle: l += '='
            elif v ==   ball: l += 'o'
            elif v ==   wall: l += '#'
            elif v ==  block: l += '@'
        print(l)

def run(d, inputs):
    screen = {}
    d += [0]*1000
    rbase = 0
    pc = 0
    output = []
    score = 0
    mem_inputs = []
    while pc < len(d):
        
        opsize = 4
        op = d[pc]
        [mode1, mode2, mode3] = get_parameter_modes(op)
        op = op % 100
        if op == 99: # halt
            opsize = 1 # unnecessary but complete
            # print(output)
            print(mem_inputs)
            return [False, score, screen]

        elif op == 1: # add
            [addr1,addr2,outAddr] = d[pc+1:pc+4]
            # size 4
            v1 = get_param_value(d, addr1, mode1, rbase)
            v2 = get_param_value(d, addr2, mode2, rbase)

            outAddr = get_write_address(outAddr, mode3, rbase)
            d[outAddr] = v1 + v2

        elif op == 2: # mul
            [addr1,addr2,outAddr] = d[pc+1:pc+4]
            # size 4
            v1 = get_param_value(d, addr1, mode1, rbase)
            v2 = get_param_value(d, addr2, mode2, rbase)
            
            
            outAddr = get_write_address(outAddr, mode3, rbase)
            d[outAddr] = v1 * v2

        elif op == 3: # input
            addr1 = d[pc+1]
            opsize = 2 
            
            update_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return [False, score, screen]
            
            pygame.display.update()
            # printscreen(screen)
            # print(score)
            time.sleep(0.015) # ~60fps
            # k = ord(getch())
            # if k == 224: k = ord(getch()) # arrow keys are 2 bytes
            # if k == 113: return [0,score,{}]
            # if len(inputs) == 0:
            #     printscreen(screen)
            #     print(score)
            #     k = ord(getch())
            #     if k == 224: k = ord(getch()) # arrow keys are 2 bytes
            #     if   k == 75: inputs.append(-1) # left
            #     elif k == 77: inputs.append(1) # right
            #     elif k ==113: # q
            #         print(mem_inputs)
            #         return [0,0,0]
            #     else: inputs.append(0)
            #     mem_inputs.append(inputs[-1])
            #hand off when unable to read anymore
            if cx_ball > lastx_paddle:
                inputs.append(1)
            elif cx_ball < lastx_paddle:
                inputs.append(-1)
            else:
                inputs.append(0)
            if len(inputs) == 0:
                raise 'got an input!'
                # return [True, pc, output]
            
            addr1 = get_write_address(addr1, mode1, rbase)

            v = inputs.pop(0)
            d[addr1] = v

        elif op == 4: # output
            addr1 = d[pc+1]
            v1 = get_param_value(d, addr1, mode1, rbase)
            opsize = 2 

            val = v1

            # output val somewhere
            output.append( val)
            
            if len(output) == 3:
                x,y,v = output
                if x == -1 and y == 0:
                    score = v
                else:
                    write_obj(output, screen)
                output = []
            
            ## after output hand off to next amp
        
        elif op == 5: # jump-if-true
            [addr1,addr2] = d[pc+1:pc+3]
            v1 = get_param_value(d, addr1, mode1, rbase)
            v2 = get_param_value(d, addr2, mode2, rbase)
            opsize = 3
            #if the first parameter is non-zero
            if v1 != 0:
                #set the instruction pointer to the value from the second parameter
                pc = v2
                continue

        elif op == 6: # jump-if-false
            [addr1,addr2] = d[pc+1:pc+3]
            v1 = get_param_value(d, addr1, mode1, rbase)
            v2 = get_param_value(d, addr2, mode2, rbase)
            opsize = 3
            #if the first parameter is zero
            if v1 == 0:
                #set the instruction pointer to the value from the second parameter
                pc = v2
                continue

        elif op == 7: # less than
            [addr1,addr2,outAddr] = d[pc+1:pc+4]
            v1 = get_param_value(d, addr1, mode1, rbase)
            v2 = get_param_value(d, addr2, mode2, rbase)
            opsize = 4
            
            outAddr = get_write_address(outAddr, mode3, rbase)
            d[outAddr] = 1 if v1 < v2 else 0

        elif op == 8: # equals
            [addr1,addr2,outAddr] = d[pc+1:pc+4]
            v1 = get_param_value(d, addr1, mode1, rbase)
            v2 = get_param_value(d, addr2, mode2, rbase)
            opsize = 4

            outAddr = get_write_address(outAddr, mode3, rbase)
            d[outAddr] = 1 if v1 == v2 else 0

        elif op == 9: # change relative base
            addr1 = d[pc+1]
            v1 = get_param_value(d, addr1, mode1, rbase)
            opsize = 2
            
            rbase += v1

        else:
            print(f'unknown op: {op} at pc: {pc}')
            return [False,-1,output]
        
        pc += opsize
        
    return [False,-1,output]

def part1(d):
    screen = run(d, [])[-1]

    bcount = list(screen.values()).count(block)
    print(f'blocks: {bcount}')

def part2(d):
    d[0] = 2
   
    score, screen = run(d, [])[1:]
    print(f'score: {score}')
part2(data)