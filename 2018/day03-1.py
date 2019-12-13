#!/usr/bin/env python3
import sys

fabric = [[0 for i in range(1000)] for j in range(1000)]
for line in sys.stdin:
    x_y, w_h = line.strip().split('@')[1].strip().split(':')
    x, y = x_y.strip().split(',')
    w, h = w_h.strip().split('x')
    
    for i in range(int(h)):
        for j in range(int(w)):
            fabric[int(y)+i][int(x)+j] += 1

count = 0
for y in range(1000):
    for x in range(1000):
        if fabric[y][x] > 1:
            count += 1
print(count)
