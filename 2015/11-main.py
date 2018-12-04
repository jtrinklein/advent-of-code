#!/usr/bin/env python3

data = 'hepxcrrq'

def has_banned_chars(p):
    return 'i' in p or 'l' in p or 'o' in p

def has_two_doubles(p):
    d = [x[0] for x in zip(p[:-1], p[1:]) if x[0] == x[1]]
    c = len(d)
    if c < 2:
        return False
    
    if c > 2:
        return True
    
    if d[0] != d[1]:
        return True
    
    return False

def has_run(p):
    c = [ord(x) for x in list(p)]
    for i in range(len(c)-2):
        v = c[i]
        if v+1 != c[i+1]:
            continue
        if v+2 != c[i+2]:
            continue
        
        return True
    return False

def is_good_pwd(p):
    return not has_banned_chars(p) and has_two_doubles(p) and has_run(p)

def inc_pwd(p):
    i = len(p) -1
    c = [ord(x) for x in list(p)]
    while i < len(p) and i > 0:
        c[i] += 1
        if c[i] > ord('z'):
            c[i] = ord('a')
            i -= 1
        else:
            return ''.join([chr(x) for x in c])
    
    return ''.join([chr(x) for x in c])

def get_next_pwd(p):
    p = inc_pwd(p)
    while not is_good_pwd(p):
        p = inc_pwd(p)
    return p

p = get_next_pwd(data)
print('part 1:', p)

p = get_next_pwd(p)
print('part 2:', p)