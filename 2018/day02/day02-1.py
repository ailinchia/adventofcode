#!/usr/bin/env python3
import sys
from collections import Counter

count_2 = 0
count_3 = 0
for line in sys.stdin:
    found_2 = False
    found_3 = False

    counter = dict(Counter(line.strip()))
    for c in counter:
        count = counter[c]
        if not found_2 and count == 2:
            count_2 += 1
            found_2 = True
        if not found_3 and count == 3:
            count_3 += 1
            found_3 = True

        if found_2 and found_3:
            break

print(count_2 * count_3)
