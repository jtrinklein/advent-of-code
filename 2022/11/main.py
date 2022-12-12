#!/usr/bin/env python3
from math import lcm
from typing import List, Tuple

data = []
class Monkey:
    items: List[int]
    op: str
    op_val: str
    test_val: int
    target_true: int
    target_false: int
    inspections: int
    id: int
    relax: bool
    def __init__(self, id:int) -> None:
        self.inspections = 0
        self.id = id
        self.relax = True

    def inspect_items(self, modval: int = None):
        self.items = [self.do_op(i, modval) for i in self.items]
        self.inspections += len(self.items)

    def do_op(self, old: int, modval: int = None) -> int:
        
        v = old
        if self.op_val != 'old':
            v = int(self.op_val)
        if self.op == '+':
            v = old + v
        else:
            v = old * v
        if self.relax:
            return v//3
        elif modval is not None:
            return v % modval
        else:
            return v
    
    def do_test(self, item) -> bool:
        _,m = divmod(item, self.test_val)
        return m == 0

    def test_items(self) -> List[Tuple[int,int]]:
        return [(item, self.target_true if self.do_test(item) else self.target_false) for item in self.items]

with open('./data.txt') as f:
    m = None
    for x in f.readlines():
        if x.startswith('Monkey'):
            data.append(Monkey(len(data)))
        elif x.startswith('  Starting'):
            data[-1].items = [int(i) for i in x.strip().split(': ')[1].split(',')]
        elif x.startswith('  Operation'):
            vals = x.strip().split(' ')
            data[-1].op = vals[-2]
            data[-1].op_val = vals[-1]
        elif x.startswith('  Test'):
            data[-1].test_val = int(x.strip().split(' ')[-1])
        elif x.startswith('    If true'):
            data[-1].target_true = int(x.strip().split(' ')[-1])
        elif x.startswith('    If false'):
            data[-1].target_false = int(x.strip().split(' ')[-1])


def part1(monkeys: List[Monkey]):
    rounds = 20
    for _ in range(rounds):
        for m in monkeys:
            m.inspect_items()
            result = m.test_items()
            m.items = []
            for item,targetId in result:
                monkeys[targetId].items.append(item)
    for m in monkeys:
        print(f'Monkey {m.id} inspected items {m.inspections} times.')
    monkeys.sort(key= lambda m: m.inspections, reverse=True)
    print(f'chase value: {monkeys[0].inspections * monkeys[1].inspections}')

def part2(monkeys: List[Monkey]):
    rounds = 10000
    for m in monkeys:
        m.relax = False

    modval = lcm(*[m.test_val for m in monkeys])
    for _ in range(rounds):

        for m in monkeys:
            m.inspect_items(modval=modval)
            result = m.test_items()
            m.items = []
            for item,targetId in result:
                monkeys[targetId].items.append(item)
    for m in monkeys:
        print(f'Monkey {m.id} inspected items {m.inspections} times.')
    monkeys.sort(key= lambda m: m.inspections, reverse=True)
    print(f'chase value: {monkeys[0].inspections * monkeys[1].inspections}')

# part1(data)
part2(data)