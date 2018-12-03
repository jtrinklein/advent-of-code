#!/usr/bin/env python3

data = None
with open('./05-data.txt') as f:
    data = f.read()

def has_banned_substr(str):
    return 'ab' in str or 'cd' in str or 'pq' in str or 'xy' in str

def has_a_repeat_pair(str):
    for i in range(len(str)-1):
        p = str[i:i+2] 
        if str.count(p) > 1:
            return True
    return False

def has_a_sandwich(str):
    for i in range(len(str)-2):
        if str[i] == str[i+2]:
            return True
    return False

def has_3_vowels(str):
    return sum([str.count(x) for x in list('aeiou')]) >= 3

def has_a_double(str):
    c = list(str)
    return len([x for x in zip(c[:-1], c[1:]) if x[0] == x[1]]) > 0
    
def is_nice(str):
    # return not has_banned_substr(str) and has_3_vowels(str) and has_a_double(str)
    return has_a_sandwich(str) and has_a_repeat_pair(str)


nice = []
naughty = []
for w in data.split('\n'):
    if is_nice(w):
        nice += [w]
    else:
        naughty += [w]

print('nice:', len(nice))
print('naughty:', len(naughty))
