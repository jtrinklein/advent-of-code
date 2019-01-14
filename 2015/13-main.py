#!/usr/bin/env python3

data = None
with open('./13-data.txt') as f:
    data = f.read().splitlines()

# data = [
#     'Alice would gain 54 happiness units by sitting next to Bob.',
#     'Alice would lose 79 happiness units by sitting next to Carol.',
#     'Alice would lose 2 happiness units by sitting next to David.',
#     'Bob would gain 83 happiness units by sitting next to Alice.',
#     'Bob would lose 7 happiness units by sitting next to Carol.',
#     'Bob would lose 63 happiness units by sitting next to David.',
#     'Carol would lose 62 happiness units by sitting next to Alice.',
#     'Carol would gain 60 happiness units by sitting next to Bob.',
#     'Carol would gain 55 happiness units by sitting next to David.',
#     'David would gain 46 happiness units by sitting next to Alice.',
#     'David would lose 7 happiness units by sitting next to Bob.',
#     'David would gain 41 happiness units by sitting next to Carol.',
# ]

happymods = {
    # part 2
    'me': {}
}
people = [
    # part 2
    'me'
]
for line in data:
    person, w, mod, amt, h, u, b, s, n, t, other = line[:-1].split()

    if person not in happymods:
        people.append(person)
        happymods[person] = {}
        #part 2
        happymods['me'][person] = 0
        happymods[person]['me'] = 0
    
    amt = int(amt)

    if mod == 'lose':
        amt = -1 * amt

    happymods[person][other] = amt

def get_path(path, rest, happyval=0):
    
    if len(rest) == 0:
        start = path[0]
        end = path[-1]
        valtostart = happymods[end][start]
        valfromstart = happymods[start][end]
        return path, happyval + valfromstart + valtostart

    bestval = happyval
    bestpath = path[:]

    for i in range(len(rest)):
        person = rest[i]
        others = rest[:]
        others.remove(person)
        valto = 0
        valfrom = 0
        if len(path) > 0:
            last = path[-1]
            # print(last, '<->', person)
            valto = happymods[last][person]
            valfrom = happymods[person][last]
        val = happyval + valto + valfrom
        newpath, newval = get_path(path + [person], others, happyval=val)

        if newval > bestval:
            bestpath = newpath
            bestval = newval
    
    return bestpath, bestval

path, happyval = get_path([], people)
print(path, happyval)
