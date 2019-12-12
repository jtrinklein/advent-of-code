#!/usr/bin/env python3

# references:
# https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
# https://bell0bytes.eu/intersection-of-line-segments/

import math
import numpy as np

with open('./03-data.txt') as f:
    [redPath,bluePath] = [x.split(',') for x in f.read().splitlines()]

print(f'r{len(redPath)}')
print(f'b{len(bluePath)}')


def build_segments(path):
    segments = []
    pos = [0,0]
    for i in path:
        segment = [pos[:]]
        dir = i[0]
        mag = int(i[1:])
        if dir == 'L' or dir == 'D':
            mag *= -1
        
        if dir == 'R' or dir == 'L':
            pos[0] += mag
        else:
            pos[1] += mag
        segment.append(pos[:])
        segments.append(segment[:])
    return segments

def are_colinear(seg0,seg1):
    [p0,q0] = seg0
    [p1,q1] = seg1
    v0 = [q0[0] - p0[0], q0[1] - p0[1]]
    v1 = [q1[0] - p1[0], q1[1] - p1[1]]
    m = np.array([ [ v0[0], -1*v1[0] ], [ v0[1], -1*v1[1] ] ])
    return np.linalg.det(m) == 0

def get_colinear_intersection(seg0,seg1):
    [p0,q0] = seg0
    [p1,q1] = seg1
    i = 0
    if p0[0] == p1[0]: # all same x values means vertical colinearity
        i = 1
    elif p0[1] != p1[1]:
        return None 

    if q0[i] < p0[i]:
        [q0,p0] = seg0
    if q1[i] < p1[i]:
        [q1,p1] = seg1

    # make sure p0 comes before p1
    if p1[i] < p0[i]:
        pt = p1[:]
        qt = q1[:]
        p1 = p0[:]
        q1 = q0[:]
        p0 = pt[:]
        q0 = qt[:]
    
    # if q0 isnt larger than p1 no intersection
    if q0[i] < p1[1]:
        return None

    # otherwise p1 is nearest intersection
    return p1

def is_vertical(seg):
    return seg[0][0] == seg[1][0]
    
def order_correctly(seg):
    [p,q] = seg
    i = 0
    if is_vertical(seg):
        i = 1
    
    if q[i] < p[i]:
        [q,p] = seg
    
    return [p,q]

def get_non_colinear_intersection(seg0, seg1):
    vseg = seg0
    hseg = seg1
    if is_vertical(hseg):
        vseg = seg1
        hseg = seg0
    [vp, vq] = order_correctly(vseg)
    [hp, hq] = order_correctly(hseg)
    
    #at this point we have perpendicular segments and we know which is horizontal and which is vertical
    if vp[1] <= hp[1] and hp[1] <= vq[1]:
        # they intesect vertically, check horizonal
        if hp[0] <= vp[0] and vp[0] <= hq[0]:
            # they intersect horizontally as well!
            return [vp[0], hp[1]]
    return None

def get_intersection(seg0, seg1):
    if are_colinear(seg0, seg1):
        return get_colinear_intersection(seg0, seg1)
    
    return get_non_colinear_intersection(seg0, seg1)

def get_dist(p1, p0):
    return sum([abs(i-j) for i,j in list(zip(p1,p0))])

def is_origin(point):
    return get_dist(point, [0,0]) == 0

# convert to segments
redSegments = build_segments(redPath)
blueSegments = build_segments(bluePath)

def part1():
    # check segments for intersection, closest wins
    dist = math.inf

    for rs in redSegments:
        for bs in blueSegments:
            i = get_intersection(rs, bs)
            if i is not None and not is_origin(i):
                print(f'intersection! rs: {rs}, bs: {bs}, i: {i}')
                iDist = get_dist(i, [0,0])
                if iDist < dist:
                    dist = iDist
                
    print(f'distance: {dist}')

def part2():
    dist = math.inf
    
    dr = 0
    for rs in redSegments:
        
        db = 0
        for bs in blueSegments:
            
            i = get_intersection(rs, bs)
            if i is not None and not is_origin(i):
                dib = get_dist(bs[0], i)
                dir = get_dist(rs[0], i)
                d = dr + db + dir + dib
                
                # print(f'intersection! rs: {rs}, bs: {bs}, i: {i}')
                if d < dist:
                    dist = d
                    print(f'shorter: {dist} at {i}')
            
            db += get_dist(bs[0], bs[1])

        dr += get_dist(rs[0], rs[1])
    print(f'fewest steps: {dist}')
part2()