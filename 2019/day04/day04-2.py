#!/usr/bin/env python3

count = 0
for i in range(357253, 892942):
    input = str(i)

    has_double = False
    has_decrease = False
    max_c = 0
    c_count = 1
    for c in input:
        ci = int(c)
        if ci < max_c:
            has_decrease = True
            break
        elif ci == max_c:
            c_count += 1
        else:
            if c_count == 2:
                has_double = True
            c_count = 1
        max_c = ci
    if c_count == 2:
        has_double = True

    if not has_decrease and has_double:
        count += 1

print(count)
