#!/usr/bin/env python3
import sys


def move_droid(direction):
    if direction == 'N':    # north
        return 1
    elif direction == 'S':  # south
        return 2
    elif direction == 'W':  # west
        return 3
    elif direction == 'E':  # east
        return 4
    else:
        assert(False)

def get_type(grids, direction, x, y):
    if direction == 'N':
        if y - 1 not in grids or x not in grids[y - 1]:
            return ''
        return grids[y-1][x]
    elif direction == 'E':
        if x + 1 not in grids[y]:
            return ''
        return grids[y][x + 1]
    elif direction == 'S':
        if y + 1 not in grids or x not in grids[y + 1]:
            return ''
        return grids[y+1][x]
    elif direction == 'W':
        if x - 1 not in grids[y]:
            return ''
        return grids[y][x-1]

def has_visited(grids, direction, x, y):
    return get_type(grids, direction, x, y) == '.'

def has_wall(grids, direction, x, y):
    return get_type(grids, direction, x, y) == '#'

def has_walls(grids, x, y):
    output = set()
    for direction in ['N', 'E', 'S', 'W']:
        if has_wall(grids, direction, x, y):
            output.add(direction)
    return output

def get_direction(grids, wall, x, y):
    if len(grids) == 0:
        return 'W', None

    walls = has_walls(grids, x, y)
    if wall == 'N':
        if 'N' not in walls:
            # move north
            if not has_visited(grids, 'W', x, y):
                return 'W', 'W'
            else:
                return 'N', 'N'
        if 'E' not in walls:
            # move east
            return 'E', 'N'
        if 'S' not in walls:
            # move south
            return 'S', 'E'
        if 'W' not in walls:
            # move west
            return 'W', 'S'
    elif wall == 'E':
        if 'E' not in walls:
            # move east
            if not has_visited(grids, 'N', x, y):
                return 'N', 'N'
            else:
                return 'E', 'E'
        if 'S' not in walls:
            # move south
            return 'S', 'E'
        if 'W' not in walls:
            # move west
            return 'W', 'S'
        if 'N' not in walls:
            # move north
            return 'N', 'W'
    elif wall == 'S':
        if 'S' not in walls:
            # move south
            if not has_visited(grids, 'E', x, y):
                return 'E', 'E'
            else:
                return 'S', 'S'
        if 'W' not in walls:
            # move west
            return 'W', 'S'
        if 'N' not in walls:
            # move north
            return 'N', 'W'
        if 'E' not in walls:
            # move east
            return 'E', 'N'
    elif wall == 'W':
        if 'W' not in walls:
            # move west
            if not has_visited(grids, 'S', x, y):
                return 'S', 'S'
            else:
                return 'W', 'W'
        if 'N' not in walls:
            # move north
            return 'N', 'W'
        if 'E' not in walls:
            # move east
            return 'E', 'N'
        if 'S' not in walls:
            # move south
            return 'S', 'E'
    elif wall == None:
        return get_direction(grids, 'E', x, y)

def update_grids(grids, direction, status, x, y):
    c = ' '
    if output == 0:
        # hit the wall
        c = '#'
    elif output == 1:
        # moved one step
        c = '.'
    elif output == 2:
        # moved one step; at location of the oxygen system
        c = 'o'
    
    dx = x
    dy = y

    if direction == 'N':
        y -= 1
    elif direction == 'S':
        y += 1
    elif direction == 'W':
        x -= 1
    else:
        x += 1
    
    if y not in grids:
        grids[y] = {}

    grids[y][x] = c

    if output != 0:
        dx = x
        dy = y

    return grids, dx, dy, c == 'o'

def print_grids(grids, dx, dy):
    min_x = None
    max_x = None
    for y in sorted(grids):
        for x in sorted(grids[y]):
            if min_x == None or x < min_x:
                min_x = x
            if max_x == None or x > max_x:
                max_x = x
    for y in sorted(grids):
        y_keys = sorted(grids[y])
        for x in range(min_x, max_x+1):
            if dy == y and dx == x:
                print('D', end='')
            elif x in y_keys:
                print(grids[y][x], end='')
            else: 
                print(' ', end='')
        print('')

    for k in range(len(grids)):
        print('\033[F', end='')

def get_pos(mode, param, relative_base):
    if mode == 0:
        return param
    elif mode == 1:
        pass
    elif mode == 2:
        return param + relative_base
    else:
        pass

def get_value(mode, param, relative_base, integers):
    if mode == 0:   # position mode
        return integers.get(get_pos(mode, param, relative_base), 0)
    elif mode == 1: # immediate mode
        return param
    elif mode == 2: # relative mode
        return integers.get(get_pos(mode, param, relative_base), 0)
    else:
        pass

for line in sys.stdin:
    items = line.strip().split(',')
    integers = { i : int(items[i]) for i in range(0, len(items)) }

    grids = {}
    x = 0
    y = 0

    ox = 0
    oy = 0

    grids[y] = {}
    grids[y][x] = '.'
    wall = None
    found_tank = False

    # program
    i = 0
    step = 0
    relative_base = 0
    while i < len(items):
        opcode = integers[i] % 100
        mode1 = int((integers[i] % 1000) / 100)
        mode2 = int((integers[i] % 10000) / 1000)
        mode3 = int((integers[i] % 100000) / 10000)
        if opcode == 1:     # adds
            integers[get_pos(mode3, integers[i + 3], relative_base)] = get_value(mode1, integers[i + 1], relative_base, integers) + get_value(mode2, integers[i + 2], relative_base, integers)
            step = 4
        elif opcode == 2:   # multiplies
            integers[get_pos(mode3, integers[i + 3], relative_base)] = get_value(mode1, integers[i + 1], relative_base, integers) * get_value(mode2, integers[i + 2], relative_base, integers)
            step = 4
        elif opcode == 3:   # input
            direction, wall = get_direction(grids, wall, x, y)
            integers[get_pos(mode1, integers[i + 1], relative_base)] = move_droid(direction)
            step = 2
        elif opcode == 4:   # output
            output = get_value(mode1, integers[i + 1], relative_base, integers)
            grids, x, y, found = update_grids(grids, direction, output, x, y)
            if found:
                found_tank = found
                ox = x
                oy = y
            if found_tank and x == 0 and y == 0:
                break
            step = 2
        elif opcode == 5:   # jump-if-true
            if get_value(mode1, integers[i + 1], relative_base, integers) != 0:
                i = get_value(mode2, integers[i + 2], relative_base, integers)
                step = 0
            else:
                step = 3
        elif opcode == 6:   # jump-if-false
            if get_value(mode1, integers[i + 1], relative_base, integers) == 0:
                i = get_value(mode2, integers[i + 2], relative_base, integers)
                step = 0
            else:
                step = 3
        elif opcode == 7:   # less than
            if get_value(mode1, integers.get(i + 1, 0), relative_base, integers) < get_value(mode2, integers[i + 2], relative_base, integers):
                integers[get_pos(mode3, integers[i + 3], relative_base)] = 1
            else:
                integers[get_pos(mode3, integers[i + 3], relative_base)] = 0
            step = 4
        elif opcode == 8:   # equals
            if get_value(mode1, integers.get(i + 1, 0), relative_base, integers) == get_value(mode2, integers[i + 2], relative_base, integers):
                integers[get_pos(mode3, integers[i + 3], relative_base)] = 1
            else:
                integers[get_pos(mode3, integers[i + 3], relative_base)] = 0
            step = 4
        elif opcode == 9:   # relative-base
            relative_base += get_value(mode1, integers.get(i + 1, 0), relative_base, integers)
            step = 2
        elif opcode == 99:
            break

        i += step

    open_paths = ['.', 'o']
    grids[0][0] = '0'
    has_dot = True
    while has_dot:
        has_dot = False
        points = []
        for y in grids:
            for x in grids[y]:
                c = grids[y][x]
                if c not in ['.', '#', ' ', 'o']:
                    if y - 1 in grids and x in grids[y - 1] and grids[y - 1][x] in open_paths:
                        points.append((c, y - 1, x))
                    if y + 1 in grids and x in grids[y + 1] and grids[y + 1][x] in open_paths:
                        points.append((c, y + 1, x))
                    if x - 1 in grids[y] and grids[y][x - 1] in open_paths:
                        points.append((c, y, x - 1))
                    if x + 1 in grids[y] and grids[y][x + 1] in open_paths:
                        points.append((c, y, x + 1))
                elif c == '.':
                    has_dot = True
        
        for (c, y, x) in points:
            grids[y][x] = str(int(c) + 1)

    print(grids[oy][ox])
    
