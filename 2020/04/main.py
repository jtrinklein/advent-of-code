#!/usr/bin/env python3
from os import replace

data = []

with open('./data.txt') as f:
    data = f.read().split('\n\n')

def get_passports(d):
    return [passport.split(' ') for passport in [line.replace('\n', ' ') for line in d]]

def has_all_fields(passport, fields):
    pfields = [p.split(':')[0] for p in passport]
    for f in fields:
        if f not in pfields:
            return False
    return True

def get_valid_passports(passportlist, fields):
    valid = [p for p in passportlist if has_all_fields(p, fields)]
    return valid

def part1(d):
    required_fields = [
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid',
        #'cid',
    ]
    passportlist = get_passports(d)

    valid_passports = get_valid_passports(passportlist, required_fields)
    print(f'{len(valid_passports)} valid passports')

part1(data)