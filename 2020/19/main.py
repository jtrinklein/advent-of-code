#!/usr/bin/env python3

import re, time

data = []

with open('./data.txt') as f:
    data = [line.strip() for line in f.readlines()]

def do_replace(s, old, replacement):
    ns = ' '.join([replacement if x == old.strip() else x for x in s.strip().split(' ')])
    return f' {ns} '

def parse_rules(ruleset):
    ordered_rules = [
        x.split(':')[-1].replace('"', '') + ' '
        for x in  
        sorted(ruleset, key= lambda r: int(r.split(':')[0]))
    ]
    
    a = ordered_rules.index(' a ')
    replaced = []
    replacers = [(str(a), 'a')]
    
    while replacers:

        old,replacement = replacers.pop()
        ordered_rules = [do_replace(r, old, replacement) for r in ordered_rules]
        replaced.append(int(old))

        for i,rule in enumerate(ordered_rules):
            if i == 0: continue
            if not any(r.isnumeric() for r in rule.strip().split(' ')) and i not in replaced:
                if '|' in rule:
                    rule = f"(?:(?:{rule.replace(' | ',')|(?:')}))"
                ordered_rules[i] = rule
                replacers.append((str(i), f'{rule.strip()}'))
    rule_0 = ordered_rules[0].replace(' ', '')
    
    return rule_0

def part1(ruleset, msgs):
    start = time.process_time()
    rule = parse_rules(ruleset)
    generate_time_s = (((time.process_time() - start)*10000000)//1)/10000000
    rerule = f'^{rule}$'
    print(rerule)
    print(f'generated in {generate_time_s} seconds')

    start = time.process_time()
    count = sum(1 if re.fullmatch(rerule, msg) else 0 for msg in msgs)
    compile_time_s = (((time.process_time() - start)*10000000)//1)/10000000

    print(f'{count} messages are valid in {compile_time_s} seconds\n')
    

# data = [
#     '0: 4 1 5',
#     '1: 2 3 | 3 2',
#     '2: 4 4 | 5 5',
#     '3: 4 5 | 5 4',
#     '4: "a"',
#     '5: "b"',
#     '',
#     'ababbb',
#     'bababa',
#     'abbbab',
#     'aaabbb',
#     'aaaabbb',
# ]

rule_definitions = data[:data.index('')]
messages = data[len(rule_definitions)+1:]

part1(rule_definitions, messages)