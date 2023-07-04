data = []
with open('./data.txt') as f:
    data = [(k[0], int(k[1:])) for k in f.read().strip().split(', ')]

dirs = [(0,1), (1, 0), (0, -1), (-1, 0)]
dir = 0

steps = dict()
for k,v in data:
    dir += 1 if k == 'R' else -1
    dir = dir % 4
    

    print(f'{k}, {v}')
