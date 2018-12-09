#!/usr/bin/env python3

data = None

with open('./07-data.txt') as f:
    data = f.read().splitlines()

dependants = []
steps = []
deptree = {}
requirements = {}
for line in data:
    parts = line.split()
    step = parts[1]
    dep = parts[-3]
    if dep not in dependants:
        dependants.append(dep)
    if step not in steps:
        steps.append(step)

    if dep not in requirements:
        requirements[dep] = []
    
    if step not in requirements[dep]:
        requirements[dep].append(step)

    if step not in deptree:
        deptree[step] = []
    
    if dep not in deptree[step]:
        deptree[step].append(dep)
    

ready = [x for x in steps if x not in dependants]
ready.sort()
def part_1():

    order = ''
    next = ready.pop(0)

    while next is not None:
        order += next
        deps = deptree.get(next, [])
        for d in deps:
            if d in order:
                requirements[d] = None
                continue
            
            reqs = requirements.get(d, [])
            
            for r in reqs:
                if r in order:
                    reqs.remove(r)
            if len(reqs) == 0:
                requirements[d] = None
                ready.append(d)

        # if next in deptree:
        #     for d in deptree[next]:
        #         if d not in ready and d not in order:
        #             ready.append(d)
        
        ready.sort()
        if len(ready) > 0:
            next = ready.pop(0)
        else:
            next = None

    print(order)

# todo: finish part 2 :(
done = False
time = 0
times = [   0,    0,    0,    0,    0]
steps = [None, None, None, None, None]
finished = ''
while not done:
    for i in range(5):
        t = times[i]
        if t > 0:
            times[i] = t - 1
        else:
            s = steps[i]
            if s == None:
                continue
            
            steps[i] = None
            finished += s
            deps = deptree.get(s, [])
            for d in deps:
                if d in finished:
                    continue
                reqs = [r for r in requirements.get(d, []) if r not in finished]

                if len(reqs) > 0:
                    continue
                ready.append(d)
                ready.sort()
    for i in range(5):
        if len(ready) > 0 and steps[i] == None:
            s = ready.pop(0)
            steps[i] = s
            times[i] = 60 + ord(s) - ord('A')
    if len([x for x in times if x > 0]) == 0 and len([x for x in steps if x != None]) == 0 and len(ready) == 0:
        done = True
    time += 1
#897 not correct....
print(time)
                    
                        