#!/usr/local/bin/python3

data = None

with open('./09-data.txt') as f:
    data = f.read().splitlines()

dists = {}
cities = []
def get_id(c1,c2):
    c = [c1, c2]
    c.sort()
    return '<->'.join(c)

for l in data:
    src,to,dest,eql,dist = l.split()
    if src not in cities:
        cities.append(src)
    if dest not in cities:
        cities.append(dest)
    id = get_id(src, dest)
    dists[id] = int(dist)

def get_weight(c1,c2):
    global dists
    id = get_id(c1,c2)
    return dists[id]

def get_path_cost(path):
    c1 = path[0]
    cost = 0
    for c2 in path[1:]:
        cost += get_weight(c1, c2)
        c1 = c2
    return cost

city_count = len(cities)




best_route = []


def get_routes(path, useLongest = False):
    global city_count
    global best_route
    global best_cost
    
    if len(path) == city_count:
        cost = get_path_cost(path)

        if (not useLongest and cost < best_cost) or (useLongest and cost > best_cost):
            # print('new best:', cost)
            best_route = path[:]
            best_cost = cost
        return
    
    for dest in cities:
        if dest in path:
            continue
        
        get_routes(path + [dest], useLongest)

route = None
routes = []

# part 1
best_cost = 10000000 # something ridiculous

for city in cities:
    path = [city]
    source = cities[:]
    cost = 0
    get_routes([city])

print('shortest:', best_cost)
# print(best_route)

# part 2
best_cost = 0

for city in cities:
    path = [city]
    source = cities[:]
    cost = 0
    get_routes([city], useLongest=True)
print('longest:', best_cost)








    
