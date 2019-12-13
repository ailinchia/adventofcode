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
    if mode == 0:   # position mode
        return integers.get(get_pos(mode, param, relative_base), 0)
    elif mode == 1: # immediate mode
        return param
    elif mode == 2: # relative mode
        return integers.get(get_pos(mode, param, relative_base), 0)
    else:
        pass

def print_grids(grids, score):
    for k in sorted(grids):
        for l in sorted(grids[k]):
            t = grids[k][l]
            if t == 0:      # empty
                print(' ', end='')
            elif t == 1:    # wall
                print('#', end='')
            elif t == 2:    # block
                print('x', end='')
            elif t == 3:    # horizontal paddle
                print('=', end='')
            elif t == 4:    # ball
                print('o', end='')
        print('')
    print(score)
    for k in range(len(grids) + 1):
        print('\033[F', end='')

def get_direction(grids):
    # get ball & horizontal paddle
    for k in sorted(grids):
        for l in sorted(grids[k]):
            t = grids[k][l]
            if t == 3:
                paddle_x = l
            elif t == 4:
                ball_x = l
    if paddle_x == ball_x:
        return 0
    elif paddle_x < ball_x:
        return 1
    else:
        return -1

# set to True to watch the game of pong
visualize = False
grids = {}
for line in sys.stdin:
    items = line.strip().split(',')
    integers = { i : int(items[i]) for i in range(0, len(items)) }

    # program
    input_signal = 0
    i = 0
    step = 0
    relative_base = 0
    output_count = 0
    x = 0
    y = 0
    score = 0
    start_print = False
    integers[0] = 2
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
            start_print = True
            integers[get_pos(mode1, integers[i + 1], relative_base)] = get_direction(grids)
            step = 2
        elif opcode == 4:   # output
            output = get_value(mode1, integers[i + 1], relative_base, integers)
            o = output_count % 3
            if o == 0:
                x = output
            elif o == 1:
                y = output
            elif o == 2:
                if x == -1 and y == 0:
                    score = output
                else:
                    if y not in grids:
                        grids[y] = {}
                    grids[y][x] = output
                    if visualize and start_print:
                        print_grids(grids, score)
            step = 2
            output_count += 1
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
    print(score)
