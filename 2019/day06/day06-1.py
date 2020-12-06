#!/usr/bin/env python3
import sys

del_keys = set()


def cleandict(ori, d, depth):
    for k, v in d.items():
        if depth > 0 and k in ori:
            del_keys.add(k)
        if len(v) > 0:
            cleandict(ori, v, depth + 1)


def iterdict(d, depth):
    global orbit_count
    for k, v in d.items():
        if len(v) > 0:
            orbit_count += depth
            iterdict(v, depth + 1)
        else:
            orbit_count += depth


orbits = {}
for line in sys.stdin:
    (object0, object1) = line.strip().split(')')
    d0 = orbits.get(object0, {})
    d1 = orbits.get(object1, {})
    d0[object1] = d1
    orbits[object0] = d0
    orbits[object1] = d1

cleandict(orbits, orbits, 0)
for del_key in del_keys:
    del orbits[del_key]

total_orbit_count = 0
for key in orbits:
    orbit_count = 0
    iterdict(orbits[key], 1)
    total_orbit_count += orbit_count

print(total_orbit_count)
