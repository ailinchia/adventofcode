#!/usr/bin/env python3
import sys

base_pattern = [0, 1, 0, -1]
for line in sys.stdin:
    line = [int(l) for l in line.strip()]
    output = []
    for phase in range(100):
        j = 1
        for l in range(len(line)):
            pos = 0
            is_first = True
            count = 0
            while pos < len(line):
                for p in base_pattern:
                    js = 0
                    if is_first:
                        is_first = False
                        js = 1

                    epos = pos + (j- js)
                    if p != 0:
                        total = sum(line[pos:epos])
                        if p == 1:
                            count += total
                        else:
                            count -= total
                    pos = epos

            j += 1
            output.append(abs(count) % 10)
    
        line = output
        output = []

    
    print(''.join([str(x) for x in line[:8]]))
