#!/usr/bin/env python3
from os import replace

data = []

with open('./data.txt') as f:
    data = f.read().split('\n\n')

def get_passports(d):
    return [passport.split(' ') for passport in [line.replace('\n', ' ') for line in d]]

def has_all_fields(passport, field_validator):
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
    pairs = [p.split(':') for p in passport]
    fieldnames = [p[0] for p in pairs]
    for f in required_fields:
        if f not in fieldnames:
            return False

    if not field_validator:
        return True
    
    return field_validator(pairs)


#    byr (Birth Year) - four digits; at least 1920 and at most 2002.
#    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
#    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
#    hgt (Height) - a number followed by either cm or in:
#        If cm, the number must be at least 150 and at most 193.
#        If in, the number must be at least 59 and at most 76.
#    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
#    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
#    pid (Passport ID) - a nine-digit number, including leading zeroes.
#    cid (Country ID) - ignored, missing or not.
def fields_are_valid(fieldpairs):
    validators = {
        'byr': lambda v: v.isdigit() and int(v) >= 1920 and int(v) <=2002,
        'iyr': lambda v: v.isdigit() and int(v) >= 2010 and int(v) <=2020,
        'eyr': lambda v: v.isdigit() and int(v) >= 2020 and int(v) <=2030,
        'hgt': lambda v: (
                v[-2:] == 'in' and v[:-2].isdigit() and int(v[:-2]) >=59 and int(v[:-2]) <= 76
            ) or (
                v[-2:] == 'cm' and v[:-2].isdigit() and int(v[:-2]) >=150 and int(v[:-2]) <= 193
            ),
        'hcl': lambda v: len(v) == 7 and v[0]=='#' and sum([1 for x in list(v[1:]) if x in '0123456789abcdef']) == 6,
        'ecl': lambda v: v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
        'pid': lambda v: len(v) == 9 and v.isdigit(),
        'cid': lambda v: True
    }
    for k,v in fieldpairs:
 
        if not validators[k](v):
            return False
    return True

def get_valid_passports(passportlist, field_validator=None):
    valid = [p for p in passportlist if has_all_fields(p, field_validator)]
    return valid

def part1(d):
    passportlist = get_passports(d)

    valid_passports = get_valid_passports(passportlist)
    print(f'{len(valid_passports)} valid passports')

def part2(d):
    valid_passports = get_valid_passports( get_passports(d), fields_are_valid )
    print(f'{len(valid_passports)} valid passports with correct fields')

part1(data)
part2(data)