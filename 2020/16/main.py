#!/usr/bin/env python3

data = []

with open('./data.txt') as f:
    data = [line.strip() for line in f.readlines()]

def parse_data(data):
    end_first_section = data.index('')
    end_second_section = data.index('', end_first_section+1)

    #get my ticket
    my_ticket = [int(x) for x in data[end_first_section+1:end_second_section][-1].split(',')]

    #build notes
    # notes for each field are:
    #  - valid value range 1
    #  - valid value range 2
    # each range is [minvalue,maxvalue] values are inclusive
    notes = {}
    for line in data[:end_first_section]:
        key,val = line.split(': ')
        notes[key] = [[int(x) for x in r.split('-')] for r in val.split(' or ')]

    #get list of other tickets
    other_tickets = [[int(x) for x in line.split(',')] for line in data[end_second_section+2:]]

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

def part1(d):
    _, ticket_list, rules = parse_data(d)
    total = 0
    for ticket in ticket_list:
        v = get_invalid_field_value(ticket, rules)
        if v:
            total += v
    print(f'sum of invalid fields: {total}')

part1(data)

