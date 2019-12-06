#!/usr/bin/env python3
import sys

image_width = 25
image_height = 6

for line in sys.stdin:
    image = [['t' for x in range(image_height)] for y in range(image_width)]

    start = 0
    while start + image_width < len(line):
        for height in range(image_height):
            for width, c in enumerate(line[start:start+image_width]):
                if c == '0':
                    # black
                    if image[width][height] == 't':
                        image[width][height] = 'x'
                elif c == '1':
                    # white
                    if image[width][height] == 't':
                        image[width][height] = ' '
                elif c == '2':
                    # transparent
                    pass
            start += image_width

    for h in range(image_height):
        for w in range(image_width):
            print(image[w][h], end='')
        print('')
