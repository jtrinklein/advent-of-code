#!/usr/bin/env python3

data = None

with open('./06-data.txt') as f:
    data = f.read().splitlines()

# data = ['1, 1', '1, 6', '8, 3', '3, 4', '5, 5','8, 9']
coords = []
max_x = 0
max_y = 0
min_x = 300
min_y = 300
for line in data:
    c= [int(x) for x in line.split(', ')]
    
    min_x = min(min_x, c[0])
    min_y = min(min_y, c[1])
    max_x = max(max_x, c[0])
    max_y = max(max_y, c[1])
    coords.append(c)

w = max_x - min_x
h = max_y - min_y

print('grid:', min_x,min_y,' =>', max_x, max_y)

def idx(x, y):
    return x + y * w

def get_dist(x, y, c):
    return abs((min_x + x) - c[0]) + abs((min_y + y) - c[1])

def part_1():
    grid = []
    areas = [0 for x in range(len(coords))]

    for y in range(h):
        grid.append([])
        for x in range(w):

            i = idx(x,y)
            location = []
            for c in coords:
                d = get_dist(x, y, c)
                location.append(d)
            minDist = min(location)

            #get the closest, if shared, its -1
            if location.count(minDist) == 1:
                owner = location.index(minDist)
                grid[y].append(owner)
                areas[owner] += 1
            else:
                grid[y].append(-1)

    largest = max(areas)
    largestOwner = areas.index(largest)
    print(largestOwner, coords[largestOwner], 'has most area:', largest)


def part_2():
    size = 0
    for x in range(w):
        for y in range(h):
            dsum = sum([get_dist(x,y,c) for c in coords])
            if dsum < 10000:
                size += 1
    print('region size:', size)

part_2()
        