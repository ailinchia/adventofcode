#!/usr/bin/env python3
import sys
from itertools import permutations 

def get_value(mode, param, integers):
    if mode == 0:
        return int(integers[int(param)])
    else:
        return int(param)

def amplifier(integers, pos, input0, input1):
    input_signal = input0
    output_signal = None

    # program
    done = False
    i = pos
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
            assert(input_signal != None)
            integers[int(integers[i + 1])] = input_signal
            input_signal = input1
            step = 2
        elif opcode == 4:   # output
            output_signal = get_value(mode1, integers[i + 1], integers)
            step = 2
            i += step
            break
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
            done = True
            break

        i += step
    return done, integers, i, output_signal

for line in sys.stdin:
    max_output_signal = 0

    for phases in permutations(range(5, 10)):
        integers = line.strip().split(',')
        amp_a = integers.copy()
        amp_a_pos = 0
        amp_b = integers.copy()
        amp_b_pos = 0
        amp_c = integers.copy()
        amp_c_pos = 0
        amp_d = integers.copy()
        amp_d_pos = 0
        amp_e = integers.copy()
        amp_e_pos = 0

        done, amp_a, amp_a_pos, output_a = amplifier(amp_a, amp_a_pos, phases[0], 0)
        done, amp_b, amp_b_pos, output_b = amplifier(amp_b, amp_b_pos, phases[1], output_a)
        done, amp_c, amp_c_pos, output_c = amplifier(amp_c, amp_c_pos, phases[2], output_b)
        done, amp_d, amp_d_pos, output_d = amplifier(amp_d, amp_d_pos, phases[3], output_c)
        done, amp_e, amp_e_pos, output_e = amplifier(amp_e, amp_e_pos, phases[4], output_d)

        while not done:
            done, amp_a, amp_a_pos, output_a = amplifier(amp_a, amp_a_pos, output_e, None)
            done, amp_b, amp_b_pos, output_b = amplifier(amp_b, amp_b_pos, output_a, None)
            done, amp_c, amp_c_pos, output_c = amplifier(amp_c, amp_c_pos, output_b, None)
            done, amp_d, amp_d_pos, output_d = amplifier(amp_d, amp_d_pos, output_c, None)
            done, amp_e, amp_e_pos, output_e = amplifier(amp_e, amp_e_pos, output_d, None)
            if output_e is not None and max_output_signal < output_e:
                max_output_signal = output_e


print(max_output_signal)
