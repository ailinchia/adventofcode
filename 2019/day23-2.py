#!/usr/bin/env python3
import sys
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
    if mode == 0:   # position mode
        return integers.get(get_pos(mode, param, relative_base), 0)
    elif mode == 1: # immediate mode
        return param
    elif mode == 2: # relative mode
        return integers.get(get_pos(mode, param, relative_base), 0)
    else:
        pass


def computer(integers, offset, inputs, outputs):
    # program
    i = offset
    step = 0
    relative_base = 0
    while i < len(integers):
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
            input_signal = -1
            if inputs:
                input_signal = inputs.pop(0)
            integers[get_pos(mode1, integers[i + 1], relative_base)] = input_signal
            step = 2
            if input_signal == -1:
                i += step
                break
        elif opcode == 4:   # output
            output = get_value(mode1, integers[i + 1], relative_base, integers)
            outputs.append(output)
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
    return integers, i, inputs, outputs


for line in sys.stdin:
    items = line.strip().split(',')
    integers = { i : int(items[i]) for i in range(0, len(items)) }

    c_integers = []
    c_offsets = []
    c_inputs = []
    c_outputs = []
    for i in range(50):
        c_integers.append(deepcopy(integers))
        c_offsets.append(0)
        c_inputs.append([i])
        c_outputs.append([])

    nat = None
    prev_nat_y = None
    while True:
        empty_count = 0
        for i in range(50):
            if not c_inputs[i]:
                empty_count += 1

            c_integers[i], c_offsets[i], c_inputs[i], c_outputs[i] = computer(c_integers[i], c_offsets[i], c_inputs[i], c_outputs[i])
            if len(c_outputs[i]) % 3 == 0:
                while len(c_outputs[i]) > 0:
                    pos = c_outputs[i].pop(0)
                    x = c_outputs[i].pop(0)
                    y = c_outputs[i].pop(0)
                    if pos == 255:
                        nat = (x, y)
                    else:
                        c_inputs[pos].append(x)
                        c_inputs[pos].append(y)
        # all empty
        if empty_count == 50:
            nat_x = nat[0]
            nat_y = nat[1]
            c_inputs[0].append(nat_x)
            c_inputs[0].append(nat_y)

            if prev_nat_y == nat_y:
                print(prev_nat_y)
                quit()

            prev_nat_y = nat_y

