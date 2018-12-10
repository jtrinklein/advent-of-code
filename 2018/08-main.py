#!/usr/bin/env python3

data = None

with open('./08-data.txt') as f:
    data = [int(x) for x in f.read().split()]

def part1(data):
    md_counts  = []
    child_counts = []
    msum = 0
    i = 0
    while i < len(data):
        c_count = data[i]
        i += 1
        md_count = data[i]
        i += 1

        while c_count == 0:
            mdend = i + md_count
            while i < mdend:
                msum += data[i]
                i += 1
            if len(child_counts) > 0:
                c_count = child_counts.pop() - 1
                md_count = md_counts.pop()
            else:
                break

        child_counts.append(c_count)
        md_counts.append(md_count)

    print('metadatas:', msum)

part1(data[:])