#!/usr/bin/env python3
import sys

for line in sys.stdin:
    for x in range(100):
        for y in range(100):
            integers = [int(x) for x in line.split(",")]

            integers[1] = x
            integers[2] = y

            # program
            for i in range(0, len(integers), 4):
                opcode = integers[i]
                if opcode == 1:
                    integers[integers[i + 3]] = integers[integers[i + 1]] + integers[integers[i + 2]]
                elif opcode == 2:
                    integers[integers[i + 3]] = integers[integers[i + 1]] * integers[integers[i + 2]]
                elif opcode == 99:
                    break

            if integers[0] == 19690720:
                print(100 * x + y)
                exit(0)

