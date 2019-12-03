data = []
debug = False
with open('./25-data.txt') as f:
    data = f.readlines()

def dist(p0, p1):
    return sum([abs(x-y) for x,y in list(zip(p0, p1))])

def id(c, p0):
    for i in range(len(c)):
        for p1 in c[i]:
            d = dist(p0, p1)
            if debug:
                print(f"{p0} => {p1} = {d}")
            if d <= 3:
                return i
    return None

def get_constellations(inData):
    c = []
    for d in inData:
        if debug:
            print(f"testing: {d}")
        p = [int(x) for x in d.strip().split(',')]
        i = id(c, p)
        
        if i is None:
            c.append([p])
        else:
            c[i].append(p)

    return c
def print_cs(clist):
    for c in clist:
        print("---------")
        for p in c:
            print(p)

def shake(cList):
    for i in range(len(cList)):
        xList = cList[:]
        c = xList.pop(i)
        for p in c:
            j = id(xList, p)
            if j is not None:
                xList[j] += c
                return xList
    return cList

def get_count():
    c = get_constellations(data)
    c2 = []

    print(f"initally found {len(c)} constellations")
    while len(c2) != len(c):
        if debug:
            print('shaking')
        c2 = c[:]
        c = shake(c)
        print(f"after shake: {len(c)} constellations")
    print(f"final constellation count: {len(c)}")
    if debug:
        print_cs(c)
get_count()
