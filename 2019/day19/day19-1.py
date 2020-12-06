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


pulls = []
for line in sys.stdin:
    items = line.strip().split(',')

    x = 0
    y = 0
    has_pull = False
    max_x = None
    min_x = 0

    start_pull = None
    end_pull = None

    while y < 50:
        integers = {i: int(items[i]) for i in range(0, len(items))}

        # program
        i = 0
        step = 0
        relative_base = 0
        input_count = 0

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
                if input_count == 0:
                    input_signal = x
                    cx = x
                    if max_x is None:
                        max_x = x + 3

                    if has_pull and max_x - 6 > x:
                        x = max_x - 6
                    else:
                        x += 1
                else:
                    input_signal = y
                    cy = y
                input_count += 1
                integers[get_pos(mode1, integers[i + 1], relative_base)] = input_signal
                step = 2
            elif opcode == 4:  # output
                output_signal = get_value(mode1, integers[i + 1], relative_base, integers)
                if output_signal == 1:
                    if not has_pull:
                        start_pull = (cy, cx)
                        has_pull = True
                        min_x = cx
                if has_pull or (max_x is not None and cx > max_x) or cx >= 49:
                    if output_signal == 0:
                        if has_pull:
                            end_pull = (cy, cx - 1)
                            pulls.append((start_pull, end_pull))
                            has_pull = False
                        max_x = cx + 3
                        y += 1
                        x = min_x
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

    total = 0
    for ((y0, x0), (y1, x1)) in pulls:
        total += (x1 - x0) + 1
    print(total)
