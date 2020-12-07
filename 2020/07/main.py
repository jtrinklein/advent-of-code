#!/usr/bin/env python3

data = []

with open('./data.txt') as f:
    data = [line.strip() for line in f.readlines()]

def get_bag_name(b):
    return b.split(' bag')[0]

def add_bag(bag, bag_db):
    #dotted cyan bags contain 3 posh fuchsia bags, 3 plaid coral bags.
    #dotted black bags contain no other bags.
    container,contents = bag.split(' contain ')
    main_bag = get_bag_name(container)
    
    bag_db[main_bag]=[]
    
    for c in contents.split(', '):
        count, rest = c.split(' ', maxsplit=1)
        if count != 'no':
            bagname = get_bag_name(rest)

            bag_db[main_bag].append((bagname, int(count)))
            #bag_db[main_bag].append(bagname)

def get_bags_db(d):
    bag_db = {}
    for line in d:
        add_bag(line, bag_db)

    return bag_db

def bag_holds(bag, target, bag_db):
    holds_target = False
    can_be_held = [b for b,c in bag_db[bag]]
    if target in can_be_held:
        return True
    for b in can_be_held:
        holds_target = holds_target or bag_holds(b, target, bag_db)
    return holds_target

def part1(d):
    db = get_bags_db(d)
    print(f'total of {len(db)} bags')
    target = 'shiny gold'
    count = sum(1 for bag in db.keys() if bag_holds(bag, target, db))

    print(f'{count} bags can eventually hold {target} bag')

def get_bag_count(bag, db):
    total = 0

    for b,c in db[bag]:
        total += c  + c * get_bag_count(b, db)

    return total

def part2(d):
    db = get_bags_db(d)
    target = 'shiny gold'
    count = get_bag_count(target, db)
    print(f'{target} contains {count} bags')
part2(data)
