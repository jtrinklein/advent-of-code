#!/usr/bin/env python3

data = list('3113322113')
print(''.join(data))
def iterate(d, times):
    for i in range(times):
        print(i)
        r = ''
        c = [d.pop(0)]
        while len(d) > 0:
            v = d.pop(0)
            if c[0] != v:
                r += str(len(c)) + c[0]
                c = []
            c.append(v)
            
        r += str(len(c)) + c[0]
        d = list(r)
    return d

# part 1
data = iterate(data, 40)
print('length after 40:', len(data))

# part 2
# really bad way.... takes a LOOONG time to run
# can be optimized using conway's elements
data = iterate(data, 10)
print('length after 50:', len(data))
