#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

@dataclass
class File:
    size: int
    name: str

@dataclass
class Dir:
    name: str
    parent: Dir
    files: List[File]
    dirs: List[Dir]
    size: int = 0

def add_subdir(d: Dir, name: str) -> Dir:
    sd = Dir(name + '/', d, [], [])
    d.dirs.append(sd)
    return sd

def add_file(d: Dir, size: int, name: str) -> File:
    f = File(size, name)
    d.files.append(f)
    p = d
    while p:
        p.size += f.size
        p = p.parent
    return f

data = []
with open('./data.txt') as f:
    data = [x.strip().split(' ') for x in f.readlines()]

def is_cmd(line: List[str]) -> bool:
    return line[0] == '$'

def is_cd(line: List[str]) -> bool:
    return line[1] == 'cd'

def build_fs(term_lines: List[List[str]]):
    root: Dir = Dir('/', None, [], [])
    current: Dir = root
    num_lines = len(term_lines)
    i = 0
    while i < num_lines:
        i += 1
        line = term_lines[i]
        if not is_cmd(line):
            raise f'should be a cmd: {line}'
        if is_cd(line):
            name = line[-1]
            if name == '..':
                current = current.parent
            else:
                current = add_subdir(current, name)
        else:
            i += 1
            while i < num_lines and not is_cmd(term_lines[i]):
                size,name = term_lines[i]
                if size != 'dir':
                    add_file(current, int(size), name)
                i += 1
            if i < num_lines:
                i -= 1

    return root

def part1(term_lines: List[List[str]]):
    root = build_fs(term_lines)
    dirs= root.dirs[:]
    total_size = 0
    while len(dirs) > 0:
        d = dirs.pop()
        dirs += d.dirs
        if d.size <= 100_000:
            total_size += d.size
    print(f'total size: {total_size}')


def part2(term_lines: List[List[str]]):
    root = build_fs(term_lines)
    dirs = root.dirs[:]
    total_size = 70000000
    unused = total_size - root.size
    required_size = 30000000
    target_size = required_size - unused
    nearest_match = total_size
    while len(dirs) > 0:
        d = dirs.pop()
        dirs += d.dirs
        if d.size >= target_size and d.size < nearest_match:
            nearest_match = d.size

    print(f'nearest_match: {nearest_match}')

# part1(data)
part2(data)