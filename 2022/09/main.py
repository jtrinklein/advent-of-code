#!/usr/bin/env python3
from typing import List,Tuple
data = []
with open('./data.txt') as f:
    data = [(x.strip()[0], int(x.strip()[2:])) for x in f.readlines()]
def print_map(v,max_x,max_y):
    max_x = max_y = 5
    for y in range(max_y, -1, -1):
        ln = ''
        for x in range(max_x+1):
            if (x,y) in v:
                ln += '#'
            else:
                ln += '.'
        print(ln)

    print(' --- ')

dbg = False
def part1(moves: List[Tuple[str,int]]):
    xx,yy = 0,0
    tx,ty = 0,0
    dx,dy = 0,0
    visited = set()
    for dir,n in moves:
        if dbg: print(dir,n)
        mx,my = 0,0
        if dir == 'R':
            mx = 1
        elif dir == 'L':
            mx = -1
        elif dir == 'U':
            my = 1
        elif dir == 'D':
            my = -1
        while n > 0:
            n -= 1
            if dbg: print(dx,dy)
            dx,dy = dx+mx, dy+my
            adx,ady = abs(dx),abs(dy)
            if dbg: print(dx,dy)
            if adx > 1 and not ady > 0:
                x = dx // adx
                dx -= x
                tx += x
            elif ady > 1 and not adx > 0:
                y = dy // ady
                dy -= y
                ty += y
            elif (adx > 1 and ady > 0) or (ady > 1 and adx > 0):
                x = dx // adx
                y = dy // ady
                dx -= x
                dy -= y
                tx,ty = tx+x, ty+y
            yy = max(yy,ty)
            xx = max(xx,tx)
            if dbg: print( dx,dy,' - ',tx,ty)
            visited.add((tx,ty))
            if dbg: print_map(visited, xx,yy)
    print(f'unique spaces: {len(visited)}')
def part2(moves: List[Tuple[str,int]]):
    xx,yy = 0,0
    tx,ty = 0,0
    dx,dy = 0,0
    d = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
    visited = set()
    for dir,n in moves:
        if dbg: print(dir,n)
        while n > 0:
            n -= 1
            mx,my = 0,0
            if dir == 'R':
                mx = 1
            elif dir == 'L':
                mx = -1
            elif dir == 'U':
                my = 1
            elif dir == 'D':
                my = -1
            for i in range(9):
                done = False
                is_tail = i == 8
                dx,dy = d[i]
                if dbg: print(d)
                dx,dy = dx+mx, dy+my
                d[i] = (dx,dy)
                adx,ady = abs(dx),abs(dy)
                if dbg: print(d)
                if adx > 1 and not ady > 0:
                    x = dx // adx
                    dx -= x
                    mx = -x
                    if is_tail: tx += x
                    d[i] = (dx,dy)
                    my = 0
                elif ady > 1 and not adx > 0:
                    y = dy // ady
                    dy -= y
                    if is_tail: ty += y
                    d[i] = (dx,dy)
                    mx = 0
                    my = -y
                elif (adx > 1 and ady > 0) or (ady > 1 and adx > 0):
                    x = dx // adx
                    y = dy // ady
                    dx -= x
                    dy -= y
                    if is_tail: tx,ty = tx+x, ty+y
                    d[i] = (dx,dy)
                    mx,my = -x,-y
                else:
                    if dbg: print(f'stop {i}')
                    done=True

                yy = max(yy,ty)
                xx = max(xx,tx)
                if dbg: print( d,' - ',tx,ty)
                
                visited.add((tx,ty))
                if dbg: print_map(visited, xx,yy)
                if done:
                    break
    print(f'unique spaces: {len(visited)}')

# part1(data)
part2(data)