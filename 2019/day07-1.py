#!/usr/bin/env python3
import sys
from itertools import permutations 

def get_value(mode, param, integers):
    if mode == 0:
        return int(integers[int(param)])
    else:
        return int(param)



for line in sys.stdin:
    max_output_signal = 0

    for phases in permutations(range(0, 5)):
        output_signal = 0
        for phase in phases:
            integers = line.split(',')
            input_signal = phase

            # program
            i = 0
            step = 0
            while i < len(integers):
                opcode = int(integers[i][-2:])
                mode1 = int(integers[i][-3:-2]) if integers[i][-3:-2] else 0
                mode2 = int(integers[i][-4:-3]) if integers[i][-4:-3] else 0
                if opcode == 1:     # adds
                    integers[int(integers[i + 3])] = str(get_value(mode1, integers[i + 1], integers) + get_value(mode2, integers[i + 2], integers))
                    step = 4
                elif opcode == 2:   # multiplies
                    integers[int(integers[i + 3])] = str(get_value(mode1, integers[i + 1], integers) * get_value(mode2, integers[i + 2], integers))
                    step = 4
                elif opcode == 3:   # input
                    integers[int(integers[i + 1])] = input_signal
                    input_signal = output_signal
                    step = 2
                elif opcode == 4:   # output
                    output_signal = get_value(mode1, integers[i + 1], integers)
                    step = 2
                elif opcode == 5:   # jump-if-true
                    if get_value(mode1, integers[i + 1], integers) != 0:
                        i = get_value(mode2, integers[i + 2], integers)
                        step = 0
                    else:
                        step = 3
                elif opcode == 6:   # jump-if-false
                    if get_value(mode1, integers[i + 1], integers) == 0:
                        i = get_value(mode2, integers[i + 2], integers)
                        step = 0
                    else:
                        step = 3
                elif opcode == 7:   # less than
                    if get_value(mode1, integers[i + 1], integers) < get_value(mode2, integers[i + 2], integers):
                        integers[int(integers[i + 3])] = "1"
                    else:
                        integers[int(integers[i + 3])] = "0"
                    step = 4
                elif opcode == 8:   # equals
                    if get_value(mode1, integers[i + 1], integers) == get_value(mode2, integers[i + 2], integers):
                        integers[int(integers[i + 3])] = "1"
                    else:
                        integers[int(integers[i + 3])] = "0"
                    step = 4
                elif opcode == 99:
                    break

                i += step
            if max_output_signal < output_signal:
                max_output_signal = output_signal
    print(max_output_signal)
