#!/usr/bin/env python3

data = None
with open('./14-data.txt') as f:
    data = f.read().splitlines()
duration = 2503

# #example
# duration = 1000
# data = [
#     'Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.',
#     'Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.',
# ]

stats = {}
rdeer = []
for line in data:
    # Dancer can fly 27 km/s for 5 seconds, but then must rest for 132 seconds.
    parts = line.split()
    name = parts[0]
    rdeer.append(name)
    stats[name] = {
        'speed': int(parts[3]),
        'flytime': int(parts[6]),
        'resttime': int(parts[-2]),
        'distance': 0,
        'flying': False,
        'timer': 0,
        'points': 0,
    }

def race(time, part2=False):
    leader = ''
    pointleader = ''
    distance = 0
    points = 0
    while time > 0:
        time -= 1
        for r in rdeer:
            flying = stats[r]['flying']
            flytime = stats[r]['flytime']
            resttime = stats[r]['resttime']
            speed = stats[r]['speed']

            if stats[r]['timer'] == 0:
                flying = not flying
                stats[r]['flying'] = flying
                stats[r]['timer'] = flytime if flying else resttime

            stats[r]['timer'] -= 1

            if flying:
                stats[r]['distance'] += speed

            if stats[r]['distance'] > distance:
                leader = r
                distance = stats[r]['distance']
        
        for r in rdeer:
            if stats[r]['distance'] == distance:
                stats[r]['points'] += 1
                if stats[r]['points'] > points:
                    points = stats[r]['points']
                    pointleader = r
    if part2: 
        return pointleader, points
    return leader, distance

def part1():
    leader, distance = race(duration)
    print(stats)
    print(f'{leader} won with a distance of {distance}')

def part2():
    leader, points = race(duration, part2=True)
    print(stats)
    print(f'{leader} won with {points} pts')

part2()
