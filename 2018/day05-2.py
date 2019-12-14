#!/usr/bin/env python3
import sys

def do_reaction(line):
    has_reaction = False

    i = 0
    while i < len(line) - 1:
        if abs(line[i] - line[i + 1]) == diff:
            has_reaction = True
            del line[i]
            del line[i]
            continue
            
        i += 1

    return has_reaction, line
    
diff = ord('a') - ord('A')

for line in sys.stdin:
    line = [ord(c) for c in line.strip()]
    
    has_reaction = True
    while has_reaction:
        has_reaction, line = do_reaction(line)
    
    min_length = None
    for o in range(ord('a'), ord('z')):
        result = [c for c in line if c != o and c + diff != o]

        has_reaction = True
        while has_reaction:
            has_reaction, result = do_reaction(result)
        
        if min_length == None or min_length > len(result):
            min_length = len(result)
            

    print(min_length)
