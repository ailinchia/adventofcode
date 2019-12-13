#!/usr/bin/env python3
import sys

total_frequency = 0
for line in sys.stdin:
    frequency = int(line)
    total_frequency += frequency
print(total_frequency)
