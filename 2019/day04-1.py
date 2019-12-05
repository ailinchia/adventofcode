#!/usr/bin/env python3

count = 0
for i in range(357253, 892942):
    input = str(i)

    has_decrease = False
    has_double = False
    max_c = 0
    for c in input:
        ci = int(c)
        if ci < max_c:
            has_decrease = True
            break
        elif ci == max_c:
            has_double = True
        max_c = ci

    if not has_decrease and has_double:
        count += 1

print(count)
