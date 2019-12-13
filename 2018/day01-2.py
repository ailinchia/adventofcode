#!/usr/bin/env python3
import sys

frequencies = []
for line in sys.stdin:
    frequencies.append(int(line))

total_frequency = 0
seen_frequencies = set()
while True:
    for frequency in frequencies:
        total_frequency += frequency
        if total_frequency in seen_frequencies:
            print(total_frequency)
            quit()

        seen_frequencies.add(total_frequency)
