#!/usr/bin/env python3
import sys


def get_value(mode, param, integers):
    if mode == 0:
        return int(integers[int(param)])
    else:
        return int(param)


for line in sys.stdin:
    integers = line.split(',')

    # program
    input = 1
    i = 0
    step = 0
    while i < len(integers):
        opcode = int(integers[i][-2:])
        mode1 = int(integers[i][-3:-2]) if integers[i][-3:-2] else 0
        mode2 = int(integers[i][-4:-3]) if integers[i][-4:-3] else 0
        if opcode == 1:
            integers[int(integers[i + 3])] = str(get_value(mode1, integers[i + 1], integers) + get_value(mode2, integers[i + 2], integers))
            step = 4
        elif opcode == 2:
            integers[int(integers[i + 3])] = str(get_value(mode1, integers[i + 1], integers) * get_value(mode2, integers[i + 2], integers))
            step = 4
        elif opcode == 3:
            integers[int(integers[i + 1])] = input
            step = 2
        elif opcode == 4:
            print(get_value(mode1, integers[i + 1], integers))
            step = 2
        elif opcode == 99:
            break

        i += step
