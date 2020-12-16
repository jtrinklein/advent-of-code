#!/usr/bin/env python3

data = []

with open('./data.txt') as f:
    data = [line.strip() for line in f.readlines()]

def parse_data(d):
    end_first_section = d.index('')
    end_second_section = d.index('', end_first_section+1)

    #get my ticket
    my_ticket = [int(x) for x in d[end_first_section+1:end_second_section][-1].split(',')]

    #build notes
    # notes for each field are:
    #  - valid value range 1
    #  - valid value range 2
    # each range is [minvalue,maxvalue] values are inclusive
    notes = {}
    for line in d[:end_first_section]:
        key,val = line.split(': ')
        notes[key] = [[int(x) for x in r.split('-')] for r in val.split(' or ')]

    #get list of other tickets
    other_tickets = [[int(x) for x in line.split(',')] for line in d[end_second_section+2:]]

    return my_ticket, other_tickets, notes

def in_range(v, r1, r2):
    return (r1[0] <= v and v <= r1[1]) or (r2[0] <= v and v <= r2[1])

def get_invalid_field_value(ticket, rules):
    for field in ticket:
        valid = False
        for rule_name in rules:
            r1,r2 = rules[rule_name]
            if in_range(field, r1, r2):
                valid = True
                break
        if not valid:
            return field
    return None

def is_valid(ticket, rules):
    v = get_invalid_field_value(ticket, rules)
    return v is None

def part1(d):
    _, ticket_list, rules = parse_data(d)
    total = 0
    invalid_count = 0
    for ticket in ticket_list:
        v = get_invalid_field_value(ticket, rules)
        if v:
            invalid_count += 1
            total += v
    print(f'invalid ticket count: {invalid_count}')
    print(f'sum of invalid fields: {total}')
    

def part2(d):
    my_ticket, other_tickets, rules = parse_data(d)
    
    #discard invalid tickets
    tickets = [t for t in other_tickets if is_valid(t, rules)]
    valid_ticket_count = len(tickets)

    field_count = len(my_ticket)

    #determine field order
    print('Determine field candidates for each rule')
    field_candiates = {}
    for rule in rules:
        print(f'checking: {rule}')
        r1,r2 = rules[rule]
        candidates = field_candiates.get(rule, [])
        for i in range(field_count):
            valid = 0
            for t in tickets:
                if in_range(t[i], r1, r2):
                    valid += 1

            if valid == valid_ticket_count:
                print(f' {i} is valid candidate')
                candidates.append(i)
        field_candiates[rule] = candidates

    print('\n-----------------\n')
    print('Deduce field order from candidates:')
    field_order = {}
    fields_identified = 0

    while fields_identified < field_count:
        identified = []
        # once we have candidates, search for rules with only 1 candidate
        for r, c in field_candiates.items():
            if len(c) == 1:
                identified.append(c[0])
                fields_identified += 1
                field_order[r] = c[0]
        # remove the fields which have assigned rules from other rule candidates
        for i in identified:
            for r,c in field_candiates.items():
                field_candiates[r] = [x for x in c if x != i]
        # repeat until we have all rules assigned
    
    for k,v in field_order.items(): print(f'{k}: {v}')
    
    print('\n-----------------\n')
    
    # field order identified
    total = 1
    for r in rules:
        if r.startswith('departure'):
            total *= my_ticket[field_order[r]]
    print(f'product of "departure" fields: {total}')

part2(data)
