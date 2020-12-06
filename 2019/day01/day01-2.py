#!/usr/bin/env python3
import sys
import math

total_fuel = 0
for line in sys.stdin:
    mass = int(line)
    fuel = math.floor(mass / 3) - 2

    while fuel > 0:
        total_fuel += fuel
        mass = fuel
        fuel = math.floor(mass / 3) - 2

print(total_fuel)
