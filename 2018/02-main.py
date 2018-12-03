#!/usr/local/bin/python3

data = None

with open('./02-data.txt') as f:
    data = f.read().splitlines()


a = list('abcdefghijklmnopqrstuvwxyz')

two = 0
three = 0

for i in range(len(data)):
    line = data[i]

    # part 1
    c = [line.count(x) for x in a]
    if 2 in c:
        two  = two + 1
    if 3 in c:
        three = three + 1
    
    
    # part 2
    data2 = data[i+1:]
    for line2 in data2:
        

        l1 = [ord(x) for x in list(line)]
        l2 = [ord(x) for x in list(line2)]
        ords = [abs(l1[x] - l2[x]) for x in range(len(l1))]
        diffs = [x for x in ords if x > 0]
        # print(diffs)
        
        if len(diffs) == 1:

            idx = ords.index(diffs[0])
            print('off by', diffs[0], 'at pos:', idx)
            print(line)
            print(line2)
            print(' '*(idx-1), '^')
            print('common characters:')
            print('id1:', line[:idx] + line[idx+1:])
            print('id2:', line2[:idx] + line2[idx+1:])
   

print('\nchksum:', two * three)
