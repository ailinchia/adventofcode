#!/usr/bin/env python3
import sys

for line in sys.stdin:
    integers = [int(x) for x in line.split(",")]

    # replace
    integers[1] = 12
    integers[2] = 2

    # program
    for i in range(0, len(integers), 4):
        opcode = integers[i]
        if opcode == 1:
            integers[integers[i + 3]] = integers[integers[i + 1]] + integers[integers[i + 2]]
        elif opcode == 2:
            integers[integers[i + 3]] = integers[integers[i + 1]] * integers[integers[i + 2]]
        elif opcode == 99:
            break

    print(integers[0])
