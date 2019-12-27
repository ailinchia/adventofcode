#!/usr/bin/env python3
import sys
from copy import deepcopy

def print_grids(grids):
    for row in grids:
        for c in row:
            print(c, end='')
        print('')

def to_string(grids):
    return ''.join([c for row in grids for c in row])
            
grids = []
for line in sys.stdin:
    line = line.strip()
    grids.append([c for c in line])

uniq_grids = set()

while True:
    new_grids = deepcopy(grids)
    for y in range(5):
        for x in range(5):
            bug_count = 0
            if x - 1 >= 0 and grids[y][x - 1] == '#':
                bug_count += 1
            if x + 1 < 5 and grids[y][x + 1] == '#':
                bug_count += 1
            if y - 1 >= 0 and grids[y - 1][x] == '#':
                bug_count += 1
            if y + 1 < 5 and grids[y + 1][x] == '#':
                bug_count += 1

            if grids[y][x] == '#':
                if bug_count != 1:
                    new_grids[y][x] = '.'
            else:
                if 1 <= bug_count <= 2:
                    new_grids[y][x] = '#'
    grids = new_grids
    grids_str = to_string(grids)
    if grids_str in uniq_grids:
        rating = 0
        for pos, c in enumerate(grids_str):
            if c == '#':
                rating += pow(2, pos)
        print(rating)
        break

    uniq_grids.add(grids_str)

