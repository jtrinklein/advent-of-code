#!/usr/bin/env python3
from datetime import datetime
data = None

with open('./04-data.txt') as f:
    data = f.read().splitlines()


logs = {}
dates = []
for line in data:
    date, log =  [x[1:] for x in line.split(']')]
    date = datetime.fromisoformat(date)
    dates.append(date)
    logs[date] = log

dates.sort()


id = None
sleeps = {}

for d in dates:
    log = logs[d]

    if log.startswith('Guard'):
        id = log.split()[1]
        
        if id not in sleeps:
            sleeps[id] = [0 for x in range(60)]
    elif log.startswith('falls'):
        start = d
    elif log.startswith('wakes'):
        for i in range(start.minute, d.minute):
            sleeps[id][i] += 1
            

    # print(d, logs[d])
def part_1(sleeps):
    best = 0
    id = 0
    minute = 0
    bmax = 0

    for k,v in sleeps.items():
        s = sum(v)
        if s > best:
            best = s
            id = k
            bmax = max(v)
            minute = v.index(bmax)
    code = int(id[1:]) * minute
    print('part 1:', id, ';', best, ';', bmax, ';', minute, '->', code)

def part_2(sleeps):
    id = 0
    best = 0
    minute = 0
    for k,v in sleeps.items():
        mx = max(v)
        if mx > best:
            id = k
            best = mx
            minute = v.index(mx)
    code = int(id[1:])*minute
    print('part 2:', id, ';', best, ';', minute, '->', code)


part_1(sleeps)

part_2(sleeps)
