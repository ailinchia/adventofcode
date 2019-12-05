#!/usr/bin/env python3

import sys

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
            slope = 'V'
        elif direction == 'L':
            x -= length
            start_x = x
            slope = 'H'
        elif direction == 'D':
            y -= length
            start_y = y
            slope = 'V'
        elif direction == 'R':
            x += length
            end_x = x
            slope = 'H'

        segments.append(((start_x, start_y, slope), (end_x, end_y, slope)))
    lineno += 1

prev_distance = None
for segment01 in segments01:
    for segment02 in segments02:
        x1 = segment01[0][0]
        y1 = segment01[0][1]
        s1 = segment01[0][2]

        x2 = segment01[1][0]
        y2 = segment01[1][1]
        s2 = segment01[1][2]

        x3 = segment02[0][0]
        y3 = segment02[0][1]
        s3 = segment02[0][2]

        x4 = segment02[1][0]
        y4 = segment02[1][1]
        s4 = segment02[1][2]

        if x1 == 0 and y1 == 0:
            continue

        if s1 == s3:
            pass
        else:
            if x1 <= x3 <= x2 and y3 <= y1 <= y4 or (x3 <= x1 <= x4 and y1 <= y3 <= y2):
                if s1 == 'H':
                    x = x3
                    y = y1
                else:
                    x = x1
                    y = y3
                distance = abs(x) + abs(y)
                if prev_distance is None:
                    prev_distance = distance

                prev_distance = min(prev_distance, distance)

print(prev_distance)
