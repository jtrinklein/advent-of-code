#!/usr/bin/env python3

import re, time

data = []

with open('./data.txt') as f:
    data = [line.strip() for line in f.readlines()]

def do_replace(s, old, replacement):
    ns = ' '.join([replacement if x == old.strip() else x for x in s.strip().split(' ')])
    return f' {ns} '

def get_ordered_rules(ruleset):
    return [
        x.split(':')[-1].replace('"', '') + ' '
        for x in  
        sorted(ruleset, key= lambda r: int(r.split(':')[0]))
    ]
    
def parse_rules(ordered_rules):
    
    
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
    return ordered_rules

def part1(ruleset, msgs):
    rules =  get_ordered_rules(ruleset)
    for i,r in enumerate(rules): print(f'{i}: {r}')
    start = time.process_time()
    rules = parse_rules(rules)
    
    rule = rules[0].replace(' ', '')
    
    generate_time_s = (((time.process_time() - start)*10000000)//1)/10000000
    
    print(f'generated in {generate_time_s} seconds')

    start = time.process_time()
    count = sum(1 if re.fullmatch(rule, msg) else 0 for msg in msgs)
    compile_time_s = (((time.process_time() - start)*10000000)//1)/10000000

    print(f'{count} messages are valid in {compile_time_s} seconds\n')

def part2(ruleset, msgs):
    rules =  get_ordered_rules(ruleset)
    
    # update 
    # 8: 42 | 42 8
    # this actually means 42 can repeat at least once
    rules[8] = ' (?: 42 )+ '

    # 11: 42 31 | 42 11 31 
    # this is going to require an equal grouping of at least 1
    # ex:
    #    (?: (?: 42 ){1} (?: 31 ){1})
    # or (?: (?: 42 ){4} (?: 31 ){4})
    # they just have to be equal and >= 1
    rules[11] = ' (?: 42 {i} 31 {i} ) '

    start = time.process_time()
    
    rules = parse_rules(rules)
    rule = rules[0].replace(' ', '')

    generate_time_s = (((time.process_time() - start)*10000000)//1)/10000000
    print(f'generated in {generate_time_s} seconds')

    count = 0
    matches = {}

    start = time.process_time()
    for i in range(1,10):
        re_rule = rule.replace('{i}',f'{{{i}}}')

        for msg in msgs:
            if msg not in matches and re.fullmatch(re_rule, msg):
                count += 1
                matches[msg] = i
            
    match_time_s = (((time.process_time() - start)*10000000)//1)/10000000

    print(f'\n{count} messages are valid in {match_time_s} seconds')


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

# data = [
#     '0: 8 11',
#     '1: "a"',
#     '2: 1 24 | 14 4',
#     '3: 5 14 | 16 1',
#     '4: 1 1',
#     '5: 1 14 | 15 1',
#     '6: 14 14 | 1 14',
#     '7: 14 5 | 1 21',
#     '8: 42',
#     '9: 14 27 | 1 26',
#     '10: 23 14 | 28 1',
#     '11: 42 31',
#     '12: 24 14 | 19 1',
#     '13: 14 3 | 1 12',
#     '14: "b"',
#     '15: 1 | 14',
#     '16: 15 1 | 14 14',
#     '17: 14 2 | 1 7',
#     '18: 15 15',
#     '19: 14 1 | 14 14',
#     '20: 14 14 | 1 15',
#     '21: 14 1 | 1 14',
#     '22: 14 14',
#     '23: 25 1 | 22 14',
#     '24: 14 1',
#     '25: 1 1 | 1 14',
#     '26: 14 22 | 1 20',
#     '27: 1 6 | 14 18',
#     '28: 16 1',
#     '29: 14',
#     '30: 14',
#     '31: 14 17 | 1 13',
#     '32: 14',
#     '33: 14',
#     '34: 14',
#     '35: 14',
#     '36: 14',
#     '37: 14',
#     '38: 14',
#     '39: 14',
#     '40: 14',
#     '41: 14',
#     '42: 9 14 | 10 1',
#     '',
#     'abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa',
#     'bbabbbbaabaabba',
#     'babbbbaabbbbbabbbbbbaabaaabaaa',
#     'aaabbbbbbaaaabaababaabababbabaaabbababababaaa',
#     'bbbbbbbaaaabbbbaaabbabaaa',
#     'bbbababbbbaaaaaaaabbababaaababaabab',
#     'ababaaaaaabaaab',
#     'ababaaaaabbbaba',
#     'baabbaaaabbaaaababbaababb',
#     'abbbbabbbbaaaababbbbbbaaaababb',
#     'aaaaabbaabaaaaababaa',
#     'aaaabbaaaabbaaa',
#     'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa',
#     'babaaabbbaaabaababbaabababaaab',
#     'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba',
# ]

rule_definitions = data[:data.index('')]
messages = data[len(rule_definitions)+1:]

part2(rule_definitions, messages)