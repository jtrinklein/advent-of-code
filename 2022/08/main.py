#!/usr/bin/env python3
from typing import List
data = []
with open('./data.txt') as f:
    data = [[int(y) for y in list(x.strip())] for x in f.readlines()]

def get_vis_map(d) -> List[List[bool]]:
    rows = len(d)
    columns = len(d[0])
    vis_map = []
    n_vis = []
    s_vis = []
    e_vis = []
    w_vis = []
    for y in range(rows):
        vis_map.append([])
        n_vis.append([])
        s_vis.append([])
        e_vis.append([])
        w_vis.append([])
        for x in range(columns):
            vis_map[y].append(False)
            n_vis[y].append(False)
            s_vis[y].append(False)
            e_vis[y].append(False)
            w_vis[y].append(False)

    h_n = [-1 for _ in range(columns)]
    h_s = [-1 for _ in range(columns)]
    h_e = [-1 for _ in range(rows)]
    h_w = [-1 for _ in range(rows)]

    for x in range(columns):
        for y in range(rows):
            n_vis[y][x] = h_n[x] < d[y][x]
            h_n[x] = max(h_n[x], d[y][x])

            s_vis[rows-y-1][x] = h_s[x] < d[rows-y-1][x]
            h_s[x] = max(h_s[x], d[rows-y-1][x])
            
            w_vis[y][x] = h_w[y] < d[y][x]
            h_w[y] = max(h_w[y], d[y][x])
            
            e_vis[y][columns-x-1] = h_e[y] < d[y][columns-x-1]
            h_e[y] = max(h_e[y], d[y][columns-x-1])

    for x in range(columns):
        for y in range(rows):
            vis_map[y][x] = n_vis[y][x] or s_vis[y][x] or w_vis[y][x] or e_vis[y][x]

    return vis_map

def part1(d):
    vis_map = get_vis_map(d)
    count = sum([x.count(True) for x in vis_map])
    print(f'visible trees: {count}')

def part2(d):
    rows = len(d)
    columns = len(d[0])
    best = 0
    bx,by= 0,0
    for y in range(rows):
        for x,h in enumerate(d[y]):
            up = 0
            for i in range(y-1, -1, -1):
                up += 1
                if d[i][x] >= h:
                    break
            down=0
            for i in range(y+1, rows):
                down += 1
                if d[i][x] >= h:
                    break
            left = 0
            for i in range(x+1, columns):
                left += 1
                if d[y][i] >= h:
                    break
            right = 0
            for i in range(x-1, -1, -1):
                right += 1
                if d[y][i] >= h:
                    break
            val = up*down*left*right

            if val > best:
                best = val
                bx = x
                by = y

    print(f'best spot at ({bx},{by}): {best}')

# part1(data)
part2(data)
#   0 1 2 3 4 5 6 - x
#   _ _ _ _ _ _ _          1: x,y = (2,1) y - 1, x - 1
#0 |_|_|_|_|_|_|_|         2: x,r-1-y = (2, (6-1)-1) = (2, 4) -> y +1, x - 1
#1 |_|_|1|_|_|_|_|
#2 |_|_|_|_|_|_|_|
#3 |_|_|_|_|_|_|_|
#4 |_|_|2|_|_|_|_|
#5 |_|_|_|_|_|_|_|
#y