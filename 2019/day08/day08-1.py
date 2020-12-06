#!/usr/bin/env python3
import sys

image_width = 25
image_height = 6

for line in sys.stdin:
    min_c0 = -1
    min_c0_c1 = 0
    min_c0_c2 = 0

    start = 0
    while start + image_width < len(line):
        c0 = 0
        c1 = 0
        c2 = 0
        for height in range(image_height):
            for c in line[start:start + image_width]:
                if c == '0':
                    c0 += 1
                elif c == '1':
                    c1 += 1
                elif c == '2':
                    c2 += 1
            start += image_width

        if min_c0 == -1 or c0 < min_c0:
            min_c0 = c0
            min_c0_c1 = c1
            min_c0_c2 = c2

print(min_c0_c1 * min_c0_c2)
