#!/usr/bin/env python3
import sys
import math

total_fuel = 0
for line in sys.stdin:
    mass = int(line)
    total_fuel += math.floor(mass / 3) - 2
print(total_fuel)
