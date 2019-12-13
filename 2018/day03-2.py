#!/usr/bin/env python3
import sys

fabric = [[0 for i in range(1000)] for j in range(1000)]
claims = []
for line in sys.stdin:
    x_y, w_h = line.strip().split('@')[1].strip().split(':')
    x, y = x_y.strip().split(',')
    w, h = w_h.strip().split('x')
    
    claims.append((int(x), int(y), int(w), int(h)))

for x, y, w, h in claims:
    for i in range(h):
        for j in range(w):
            fabric[y+i][x+j] += 1

for d, (x, y, w, h) in enumerate(claims):
    overlap = False
    for i in range(h):
        for j in range(w):
            if fabric[y+i][x+j] != 1:
                overlap = True
                break
        if overlap:
            break
    if not overlap:
        print(d + 1)
        quit()
