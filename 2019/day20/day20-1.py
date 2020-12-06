#!/usr/bin/env python3
import sys
from copy import deepcopy


def find_edges(grids, min_x, max_x, min_y, max_y, c):
    upper_y = 0
    left_x = 0
    found_left = False
    right_x = 0
    found_right = False
    for y in range(min_y, max_y):
        row = grids[y]
        for x in range(min_x, max_x):
            if row[x] == c:
                found_left = True
                left_x = x
                break
        for x in range(max_x - 1, left_x, -1):
            if row[x] == c:
                found_right = True
                right_x = x
                break
        if found_left and found_right:
            upper_y = y
            break

    lower_y = 0
    found_lower = False
    for y in range(max_y - 1, upper_y, -1):
        row = grids[y]
        for x in range(min_x, max_x):
            if row[x] == c:
                found_lower = True
                lower_y = y
                break

        if found_lower:
            break

    return (upper_y, lower_y, left_x, right_x)


def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


def get_paths(grids, gates0, gates1, paths, distances):
    for g0 in sorted(gates0):
        gs = deepcopy(grids)
        (y, x) = gates0[g0]
        gs[y][x] = '0'

        has_changes = True
        while has_changes:
            has_dot = False
            points = []
            for y in range(upper_y, lower_y + 1):
                row = gs[y]
                for x in range(left_x, right_x + 1):
                    if inner_upper_y < y < inner_lower_y and inner_left_x < x < inner_right_x:
                        continue

                    c = row[x]
                    if c not in ['.', '#']:
                        if y - 1 >= 0 and gs[y - 1][x] == '.':
                            points.append((c, y - 1, x))
                        if y + 1 < len(gs) and gs[y + 1][x] == '.':
                            points.append((c, y + 1, x))
                        if x - 1 >= 0 and gs[y][x - 1] == '.':
                            points.append((c, y, x - 1))
                        if x + 1 < len(row) and gs[y][x + 1] == '.':
                            points.append((c, y, x + 1))

            for (c, y, x) in points:
                gs[y][x] = str(int(c) + 1)

            has_changes = len(points) > 0

        for g1 in sorted(gates1):
            (g1y, g1x) = gates1[g1]
            if gs[g1y][g1x] != '.':
                arr = paths.get(g0, [])
                arr.append(g1)
                paths[g0] = arr
                d = distances.get(g0, {})
                d[g1] = int(gs[g1y][g1x])
                distances[g0] = d

        for g00 in sorted(gates0):
            if g00 == g0:
                continue

            (g0y, g0x) = gates0[g00]
            if gs[g0y][g0x] != '.':
                arr = paths.get(g0, [])
                arr.append(g00)
                paths[g0] = arr
                d = distances.get(g0, {})
                d[g00] = int(gs[g0y][g0x])
                distances[g0] = d
    return paths, distances


grids = []
for line in sys.stdin:
    grids.append([c for c in line[:-1]])

# find outer edges
upper_y, lower_y, left_x, right_x = find_edges(grids, 0, len(grids[0]), 0, len(grids), '#')

# find inner edges
inner_upper_y, inner_lower_y, inner_left_x, inner_right_x = find_edges(grids, left_x, right_x, upper_y, lower_y, ' ')
inner_upper_y -= 1
inner_lower_y += 1
inner_left_x -= 1
inner_right_x += 1

# outer gates
outer_gates = {}

# horizontal
for y in range(upper_y, lower_y):
    gl = ''.join(grids[y][0:left_x])
    gr = ''.join(grids[y][right_x + 1:])
    if gl != '  ':
        outer_gates[gl] = (y, left_x)
    if gr != '  ':
        outer_gates[gr] = (y, right_x)

# vertical
for x in range(left_x, right_x):
    gu = ''.join([grids[0][x], grids[1][x]])
    gl = ''.join([grids[lower_y + 1][x], grids[lower_y + 2][x]])
    if gu != '  ':
        outer_gates[gu] = (upper_y, x)
    if gl != '  ':
        outer_gates[gl] = (lower_y, x)

# inner gates
inner_gates = {}

# horizontal
for y in range(inner_upper_y + 1, inner_lower_y):
    gl = ''.join(grids[y][inner_left_x + 1:inner_left_x + 3])
    gr = ''.join(grids[y][inner_right_x - 2:inner_right_x])
    if len(gl.strip()) == 2:
        inner_gates[gl] = (y, inner_left_x)
    if len(gr.strip()) == 2:
        inner_gates[gr] = (y, inner_right_x)

# vertical
for x in range(inner_left_x + 1, inner_right_x):
    gu = ''.join([grids[inner_upper_y + 1][x], grids[inner_upper_y + 2][x]])
    gl = ''.join([grids[inner_lower_y - 2][x], grids[inner_lower_y - 1][x]])
    if len(gu.strip()) == 2:
        inner_gates[gu] = (inner_upper_y, x)
    if len(gl.strip()) == 2:
        inner_gates[gl] = (inner_lower_y, x)

# shortest path from AA to ZZ
paths = {}
distances = {}
paths, distances = get_paths(grids, outer_gates, inner_gates, paths, distances)
paths, distances = get_paths(grids, inner_gates, outer_gates, paths, distances)
all_paths = find_all_paths(paths, 'AA', 'ZZ')

min_count = None
min_path = None
for ap in all_paths:
    count = 0
    for i, p in enumerate(ap):
        if i == len(ap) - 1:
            break
        count += distances[p][ap[i + 1]]
    count += len(ap) - 2
    if min_count is None or min_count > count:
        min_count = count
        min_path = ap

print(min_count, min_path)
