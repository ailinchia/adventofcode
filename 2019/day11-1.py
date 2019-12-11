#!/usr/bin/env python3
import sys


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return 'Point(' + str(self.x) + ', ' + str(self.y) + ')'

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


directions = ['U', 'R', 'D', 'L']

for line in sys.stdin:
    items = line.strip().split(',')
    integers = { i : int(items[i]) for i in range(0, len(items)) }

    panels = {}

    # program
    i = 0
    j = 0
    
    direction_pos = 0
    color = 0
    point_robot = Point(0, 0)

    step = 0
    relative_base = 0

    paint_count = 0

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
            input_signal = 0
            if str(point_robot) in panels:
                input_signal = panels[str(point_robot)]
            integers[get_pos(mode1, integers[i + 1], relative_base)] = input_signal
            step = 2
        elif opcode == 4:   # output
            output = get_value(mode1, integers[i + 1], relative_base, integers)
            if j % 2 == 0:
                # color
                color = output
                if str(point_robot) not in panels:
                    paint_count += 1

                panels[str(point_robot)] = color
            else:
                ori_direction_pos = direction_pos
                # direction
                if output == 0:
                    # left 90 degree
                    direction_pos -= 1
                    if direction_pos < 0:
                        direction_pos += len(directions)
                else:
                    # right 90 degree
                    direction_pos += 1
                    if direction_pos >= len(directions):
                        direction_pos -= len(directions)

                # move robot
                if directions[direction_pos] == 'U':
                    point_robot.y -= 1
                elif directions[direction_pos] == 'R':
                    point_robot.x += 1
                elif directions[direction_pos] == 'D':
                    point_robot.y += 1
                elif directions[direction_pos] == 'L':
                    point_robot.x -= 1
            j += 1
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
    print(paint_count)
