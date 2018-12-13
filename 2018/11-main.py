#!/usr/bin/env python3

data = 9306

gridsize = 300
grid = []
for y in range(1, gridsize+1):
    grid.append([])
    for x in range(1, gridsize+1):
        #Find the fuel cell's rack ID, which is its X coordinate plus 10.
        id = x + 10
        
        #Begin with a power level of the rack ID times the Y coordinate.
        level = id * y

        #Increase the power level by the value of the grid serial number (your puzzle input).
        level += data
        #Set the power level to itself multiplied by the rack ID.
        level *= id
        #Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
        hval = int(('000' + str(abs(level)))[-3])
        #Subtract 5 from the power level.
        grid[y-1].append(hval - 5)

maxlvl = -9
X = 0
Y = 0
S = 0
for size in range(1, 300):
    print('size:', size)
    for y in range(1, gridsize - size + 1):
        for x in range(1, gridsize - size + 1):
            lvl = 0
            
            for yi in range(0, size):
                lvl += sum(grid[y + yi - 1][x - 1:x - 1 + size])
                
            if lvl > maxlvl:
                maxlvl = lvl
                X = x
                Y = y
                S = size
print('33,45')
print(maxlvl, ' at ', str(X) + ',' + str(Y) + ',' + str(S))