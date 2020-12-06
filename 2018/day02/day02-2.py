#!/usr/bin/env python3
import sys
from collections import Counter

box_ids = []
for line in sys.stdin:
    box_id = line.strip()
    box_ids.append((box_id, Counter(box_id)))

for id0, c0 in box_ids:
    for id1, c1 in box_ids:
        diff = c0 - c1
        if len(diff) == 1:
            pairs = diff.most_common()[0]
            if pairs[1] == 1:
                print(id0.replace(pairs[0], ''))
                quit()
