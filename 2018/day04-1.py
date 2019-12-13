#!/usr/bin/env python3
import sys

records = []
for line in sys.stdin:
    records.append(line.strip())

guards = {}
guard = 0
for record in sorted(records):
    activity = record[-2:]
    if activity == 'ft':
        # starts shift
        guard = record[26:30].strip()
    elif activity == 'up':
        # wakes up
        min_up = int(record[15:17])

        if guard not in guards:
            guards[guard] = [0 for x in range(60)]

        for m in range(min_down, min_up):
            guards[guard][m] += 1
    elif activity == 'ep':
        # sleeps
        min_down = int(record[15:17])

max_sleep = 0
max_sleep_min = 0
bad_guard = 0
for guard in guards:
    sleep = sum(guards[guard])
    if max_sleep < sleep:
        max_sleep = sleep
        bad_guard = guard
        max_sleep_min_count = 0
        for m, c in enumerate(guards[guard]):
            if c > max_sleep_min_count:
                max_sleep_min_count = c
                max_sleep_min = m

print(int(bad_guard) * max_sleep_min)
