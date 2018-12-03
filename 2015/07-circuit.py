#!/usr/bin/env python3

"""
This is one solution which is not my own.
I don't remember the source though. I went through a couple different ones.
I'm still trying to understand the solution before I personalize it.
"""

data = None

with open('./07-data.txt') as f:
    data = f.read().splitlines()


# data = '123 -> x\n456 -> y\nx AND y -> d\nx OR y -> e\nx LSHIFT 2 -> f\ny RSHIFT 2 -> g\nNOT x -> h\nNOT y -> i'
# data = 'x AND y -> a\n3 -> x\n5 -> y'

mem = {}

def tryval(v):
    try:
        return int(v)
    except:
        return
   
while('a' not in mem):
    for i in data:
        e,d = i.split(' -> ')
        if d is 'b':
            pass
        try:
            if 'NOT' in e:
                b = e.split()[-1]
                mem[d] = 65535 - mem.get(b, tryval(b))
            elif 'AND' in e:
                a,b = e.split(' AND ')
                mem[d] = mem.get(a, tryval(a)) & mem.get(b, tryval(b))
            elif 'OR' in e:
                a,b = e.split(' OR ')
                mem[d] = mem.get(a, tryval(a)) | mem.get(b, tryval(b))
            elif 'LSHIFT' in e:
                a,b = e.split(' LSHIFT ')
                mem[d] = (mem.get(a, tryval(a)) << mem.get(b, tryval(b))) & 65535
            elif 'RSHIFT' in e:
                a,b = e.split(' RSHIFT ')
                mem[d] = (mem.get(a, tryval(a)) >> mem.get(b, tryval(b))) & 65535
            elif e in mem:
                mem[d] = mem.get(e, tryval(e))
            else:
                mem[d] = int(e)
        except:
            pass
        
# print(mem)
print('a:', mem.get('a'))
