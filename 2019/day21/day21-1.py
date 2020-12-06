#!/usr/bin/env python3
import sys


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


for line in sys.stdin:
    items = line.strip().split(',')
    integers = {i: int(items[i]) for i in range(0, len(items))}

    grids = []
    grids.append([])
    x = 0
    y = 0

    # T temp register
    # J jump register
    # 
    # A has ground 1 tile away
    # B has ground 2 tile away
    # C has ground 3 tile away
    # D has ground 4 tile away
    # 
    # AND X Y sets Y to true if both X and Y are true; otherwise, it sets Y to false.
    # OR X Y sets Y to true if at least one of X or Y is true; otherwise, it sets Y to false.
    # NOT X Y sets Y to true if X is false; otherwise, it sets Y to false.
    instructions = '''NOT C T
OR D J
AND T J
NOT A T
OR T J
WALK
'''

    input_signals = [ord(c) for c in instructions]

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
            integers[get_pos(mode1, integers[i + 1], relative_base)] = input_signals.pop(0)
            step = 2
        elif opcode == 4:  # output
            output = get_value(mode1, integers[i + 1], relative_base, integers)
            if output < 0xff:
                c = chr(output)
                if output == 10:
                    y += 1
                    grids.append([])
                else:
                    grids[y].append(c)
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

    for y in range(len(grids) - 1, -1, -1):
        if len(grids[y]) == 0:
            del grids[y]

    for y in range(len(grids)):
        for x in range(len(grids[y])):
            print(grids[y][x], end='')
        print('')
