#!/usr/bin/env python3
import sys

diff = ord('a') - ord('A')
for line in sys.stdin:
    line = [ord(c) for c in line.strip()]
    has_reaction = True
    while has_reaction:
        has_reaction = False
        i = 0
        while i < len(line) - 1:
            if abs(line[i] - line[i + 1]) == diff:
                has_reaction = True
                del line[i]
                del line[i]
                continue
            
            i += 1
    print(len(line))
