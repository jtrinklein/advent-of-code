#!/usr/bin/env python3
from __future__ import annotations
from typing import List, Tuple
from dataclasses import dataclass
from collections import deque

@dataclass
class Node:
    x: int
    y: int
    dist: int = 0
    path_pos: int = 0
    score: int = 0
    parent: Node = None

    def __eq__(self, __o: Node) -> bool:
        return self.x == __o.x and self.y == __o.y
    
    def __lt__(self, other:Node) -> bool:
        return self.score < other.score
    
    def __gt__(self, other:Node) -> bool:
        return self.score > other.score

data = []

with open('./data.txt') as f:
    data = [[ord(y)-ord('a') if y.islower() else ord(y) for y in list(x.strip())] for x in f.readlines()]


def bfs(d:List[List[int]], reverse=False) -> List[Tuple[int,int]]:
    ymax = len(d)
    xmax = len(d[0])
    start,end  = None,None
    s = ord('S')
    e = ord('E')
    for y,r in enumerate(d):
        for x,p in enumerate(r):
            if p == s: start=Node(x,y)
            if p == e: end = Node(x,y)
    d[start.y][start.x] = 0
    d[end.y][end.x] = ord('z')-ord('a')
    
    
    q = deque()
    visited:List[Node] = []
    in_range = lambda x,y: (0<=x<xmax)and(0<=y<ymax)
    forward_test = lambda x,y,h,d: in_range(x,y)and(d[y][x]<=h+1)
    reverse_test = lambda x,y,h,d: in_range(x,y)and(h-1<=d[y][x])
    test = None
    end_test = lambda n: n == end
    if reverse:
        q.append(end)
        visited.append(end)
        test = reverse_test
        end_test = lambda n: d[n.y][n.x] == 0
    else:
        q.append(start)
        visited.append(start)
        test = forward_test
    while len(q) > 0:
        cur = q.popleft()
        if end_test(cur)    :
            return get_path(cur)
        h = d[cur.y][cur.x]
        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            x,y = cur.x+dx,cur.y+dy
            if test(x,y,h,d):
                child = Node(x,y)
                if child not in visited:
                    child.parent = cur
                    visited.append(child)
                    q.append(child)

    return None

def get_path(node: Node) -> List[Tuple[int,int]]:
    path = []
    c = node
    while c is not None:
        path.append((c.x,c.y))
        c = c.parent
    return path[::-1]


def part1(d: List[List[int]]):
    path = bfs(d)
    steps = len(path)-1 
    print(f'best path length: {len(path)} best number of steps: {steps}')


def part2(d):
    path = bfs(d, reverse=True)
    steps = len(path)-1 
    print(f'best path length: {len(path)} best number of steps: {steps}')

# part1(data)
part2(data)