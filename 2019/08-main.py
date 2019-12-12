#!/usr/bin/env python3

data = None

with open('./08-data.txt') as f:
    data = [int(x) for x in list(f.read())]

w = 25
h = 6
layer_size = w*h

def part1(data):
    layer = data[:layer_size]
    data = data[layer_size:]
    zero_count = layer.count(0)

    while len(data) > 0:
        l = data[:layer_size]
        data = data[layer_size:]
        zc = l.count(0)

        if zc < zero_count:
            layer = l[:]
            zero_count = zc

    print(layer.count(1) * layer.count(2))

# part1(data[:])
black = 0
white = 1
transparent = 2

def draw_img(img):
    for y in range(h):
        line = ''
        for x in range(w):
            p = img[y*w + x]
            if p == black or p == transparent:
                line += '-'
            else:
                line += '#'
        print(line)

def part2(data):
    img = [None]*layer_size
    while img.count(None) > 0 and len(data) > 0:
        layer = data[:layer_size]
        data = data[layer_size:]

        for i in range(layer_size):
            if img[i] is None and layer[i] != transparent:
                img[i] = layer[i]
            
    draw_img(img)

part2(data[:])
