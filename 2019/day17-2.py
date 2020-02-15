#!/usr/bin/env python3
import sys
from itertools import combinations, permutations
from copy import deepcopy


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
    if mode == 0:  # position mode
        return integers.get(get_pos(mode, param, relative_base), 0)
    elif mode == 1:  # immediate mode
        return param
    elif mode == 2:  # relative mode
        return integers.get(get_pos(mode, param, relative_base), 0)
    else:
        pass


def robots(integers, inputs):
    grids = []
    grids.append([])
    x = 0
    y = 0

    # robot position
    rx = 0
    ry = 0

    # program
    i = 0
    step = 0
    relative_base = 0
    while i < len(items):
        opcode = integers[i] % 100
        mode1 = int((integers[i] % 1000) / 100)
        mode2 = int((integers[i] % 10000) / 1000)
        mode3 = int((integers[i] % 100000) / 10000)
        if opcode == 1:  # adds
            integers[get_pos(mode3, integers[i + 3], relative_base)] = get_value(mode1, integers[i + 1], relative_base, integers) + get_value(mode2, integers[i + 2], relative_base, integers)
            step = 4
        elif opcode == 2:  # multiplies
            integers[get_pos(mode3, integers[i + 3], relative_base)] = get_value(mode1, integers[i + 1], relative_base, integers) * get_value(mode2, integers[i + 2], relative_base, integers)
            step = 4
        elif opcode == 3:  # input
            integers[get_pos(mode1, integers[i + 1], relative_base)] = inputs.pop(0)
            step = 2
        elif opcode == 4:  # output
            output = get_value(mode1, integers[i + 1], relative_base, integers)
            if output < 0xff:
                c = chr(output)
                if output == 10:
                    y += 1
                    x = 0
                    grids.append([])
                else:
                    if c == '^':
                        rx = x
                        ry = y
                    grids[y].append(c)
                    x += 1
            else:
                print(output)
            step = 2
        elif opcode == 5:  # jump-if-true
            if get_value(mode1, integers[i + 1], relative_base, integers) != 0:
                i = get_value(mode2, integers[i + 2], relative_base, integers)
                step = 0
            else:
                step = 3
        elif opcode == 6:  # jump-if-false
            if get_value(mode1, integers[i + 1], relative_base, integers) == 0:
                i = get_value(mode2, integers[i + 2], relative_base, integers)
                step = 0
            else:
                step = 3
        elif opcode == 7:  # less than
            if get_value(mode1, integers.get(i + 1, 0), relative_base, integers) < get_value(mode2, integers[i + 2], relative_base, integers):
                integers[get_pos(mode3, integers[i + 3], relative_base)] = 1
            else:
                integers[get_pos(mode3, integers[i + 3], relative_base)] = 0
            step = 4
        elif opcode == 8:  # equals
            if get_value(mode1, integers.get(i + 1, 0), relative_base, integers) == get_value(mode2, integers[i + 2], relative_base, integers):
                integers[get_pos(mode3, integers[i + 3], relative_base)] = 1
            else:
                integers[get_pos(mode3, integers[i + 3], relative_base)] = 0
            step = 4
        elif opcode == 9:  # relative-base
            relative_base += get_value(mode1, integers.get(i + 1, 0), relative_base, integers)
            step = 2
        elif opcode == 99:
            break

        i += step

    return grids, rx, ry


for line in sys.stdin:
    items = line.strip().split(',')
    integers = {i: int(items[i]) for i in range(0, len(items))}

    integers[0] = 1
    grids, rx, ry = robots(deepcopy(integers), [])

    for y in range(len(grids) - 1, -1, -1):
        if len(grids[y]) == 0:
            del grids[y]

    paths = []
    x = rx
    y = ry
    facing = 'U'
    direction = None
    prev_direction = None
    done = False
    count = 0
    while not done:
        changed = True
        if facing == 'U':
            if y - 1 >= 0 and grids[y - 1][x] == '#':
                # up
                changed = False
                count += 1
                y -= 1
                facing = 'U'
            elif x + 1 < len(grids[y]) and grids[y][x + 1] == '#':
                # right
                direction = 'R'
                x += 1
                facing = 'R'
            elif x - 1 >= 0 and grids[y][x - 1] == '#':
                # left
                direction = 'L'
                x -= 1
                facing = 'L'
            else:
                done = True
        elif facing == 'R':
            if x + 1 < len(grids[y]) and grids[y][x + 1] == '#':
                # right
                changed = False
                count += 1
                x += 1
                facing = 'R'
            elif y + 1 < len(grids) and grids[y + 1][x] == '#':
                # down
                direction = 'R'
                y += 1
                facing = 'D'
            elif y - 1 >= 0 and grids[y - 1][x] == '#':
                # up
                direction = 'L'
                y -= 1
                facing = 'U'
            else:
                done = True
        elif facing == 'D':
            if y + 1 < len(grids) and grids[y + 1][x] == '#':
                # down
                changed = False
                count += 1
                y += 1
                facing = 'D'
            elif x + 1 < len(grids[y]) and grids[y][x + 1] == '#':
                # right
                direction = 'L'
                x += 1
                facing = 'R'
            elif x - 1 >= 0 and grids[y][x - 1] == '#':
                # left
                direction = 'R'
                x -= 1
                facing = 'L'
            else:
                done = True
        elif facing == 'L':
            if x - 1 >= 0 and grids[y][x - 1] == '#':
                # left
                changed = False
                count += 1
                x -= 1
                facing = 'L'
            elif y + 1 < len(grids) and grids[y + 1][x] == '#':
                # down
                direction = 'L'
                y += 1
                facing = 'D'
            elif y - 1 >= 0 and grids[y - 1][x] == '#':
                # up
                direction = 'R'
                y -= 1
                facing = 'U'
            else:
                done = True

        if prev_direction is None:
            prev_direction = direction

        if not done and changed and count != 0:
            paths.append(prev_direction + ',' + str(count + 1))
            prev_direction = direction
            count = 0

    path = ','.join(paths)

    possibles = []
    for length in range(22, 6, -1):
        i = 0
        while i + length <= len(path):
            ss = path[i:i + length]
            if (i == 0 or path[i - 1] == ',') and '0' <= ss[-1:] <= '9' and (ss[0] == 'L' or ss[0] == 'R'):
                possibles.append(ss)
            i += 1

    done = False
    uniq_sets = set()
    tuples = list(combinations(possibles, 3))
    for t in tuples:
        for A, B, C in list(permutations(t)):
            if (A, B, C) in uniq_sets:
                continue

            uniq_sets.add((A, B, C))

            output = path
            output = output.replace(A, 'A')
            output = output.replace(B, 'B')
            output = output.replace(C, 'C')

            if len(output) <= 30:
                pos_l = output.find('L')
                pos_r = output.find('R')
                if pos_l >= 0 or pos_r >= 0:
                    if pos_l >= 0 and pos_r >= 0:
                        pos = min(pos_l, pos_r)
                    elif pos_l >= 0:
                        pos = pos_l
                    else:
                        pos = pos_r
                    s = output[pos:]
                    if A.startswith(s):
                        output = output[:pos] + 'A'
                    elif B.startswith(s):
                        output = output[:pos] + 'B'
                    elif C.startswith(s):
                        output = output[:pos] + 'C'

            if 'L' not in output and 'R' not in output:
                done = True
                break

        if done:
            break

    input_str = output + '\n' + A + '\n' + B + '\n' + C + '\n' + 'n\n'
    inputs = [ord(c) for c in input_str]

    integers[0] = 2
    grids, rx, ry = robots(deepcopy(integers), inputs)
