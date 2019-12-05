#!/usr/bin/env python3

import sys


def get_slope(d):
    if d == 'U' or d == 'D':
        return 'V'
    else:
        return 'H'


def get_diff(d, x1, y1, x2, y2):
    if d == 'U':
        return abs(y - max(y1, y2))
    elif d == 'D':
        return abs(y - min(y1, y2))
    elif d == 'L':
        return abs(x - min(x1, x2))
    elif d == 'R':
        return abs(x - max(x1, x2))


segments01 = []
segments02 = []
lineno = 0
for line in sys.stdin:
    x = 0
    y = 0

    if lineno == 0:
        segments = segments01
    else:
        segments = segments02

    for path in line.split(','):
        direction = path[0]
        length = int(path[1:])

        start_x = x
        start_y = y

        end_x = x
        end_y = y

        if direction == 'U':
            y += length
            end_y = y
        elif direction == 'L':
            x -= length
            start_x = x
        elif direction == 'D':
            y -= length
            start_y = y
        elif direction == 'R':
            x += length
            end_x = x

        segments.append(((start_x, start_y, direction, length), (end_x, end_y, direction, length)))
    lineno += 1

prev_steps = None
length01 = 0
for segment01 in segments01:
    x1 = segment01[0][0]
    y1 = segment01[0][1]
    d1 = segment01[0][2]
    l1 = segment01[0][3]

    x2 = segment01[1][0]
    y2 = segment01[1][1]
    d2 = segment01[1][2]
    l2 = segment01[1][3]

    length01 += l1

    if x1 == 0 and y1 == 0:
        continue

    length02 = 0
    for segment02 in segments02:
        x3 = segment02[0][0]
        y3 = segment02[0][1]
        d3 = segment02[0][2]
        l3 = segment02[0][3]

        x4 = segment02[1][0]
        y4 = segment02[1][1]
        d4 = segment02[1][2]
        l4 = segment02[1][3]

        length02 += l3
        if get_slope(d1) == get_slope(d3):
            pass
        else:
            # print((x1, y1), (x2, y2), (x3, y3), (x4, y4))
            if x1 <= x3 <= x2 and y3 <= y1 <= y4 or (x3 <= x1 <= x4 and y1 <= y3 <= y2):
                if get_slope(d1) == 'H':
                    x = x3
                    y = y1
                else:
                    x = x1
                    y = y3

                lengthdiff = get_diff(d1, x1, y1, x2, y2) + get_diff(d3, x3, y3, x4, y4)
                steps = length01 + length02 - lengthdiff
                if prev_steps is None:
                    prev_steps = steps

                prev_steps = min(prev_steps, steps)

print(prev_steps)
