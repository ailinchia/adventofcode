#!/usr/bin/env python3
import sys
import math
from itertools import combinations

def lcm(n1, n2):
    return (n1 * n2) // math.gcd(n1, n2)

def get_velocity(p0, p1):
    if p0 == p1:
        return 0
    elif p0 > p1:
        return -1
    else:
        return 1

def apply_velocity(points, pairs):
    # calculate velocity
    for i, (k0, k1) in enumerate(pairs):
        m0, v0 = points[k0]
        m1, v1 = points[k1]

        v0 += get_velocity(m0, m1)
        v1 += get_velocity(m1, m0)

        points[k0] = (m0, v0)
        points[k1] = (m1, v1)

    # apply velocity
    for key in points:
        m, v = points[key]
        points[key] = (m + v, v)

    return points

initial_x = {}
initial_y = {}
initial_z = {}

keys = []
points_x = {}
points_y = {}
points_z = {}
for line in sys.stdin:
    xs, ys, zs = line.strip()[1:-1].split(',')
    
    x = int(xs.strip()[2:])
    y = int(ys.strip()[2:])
    z = int(zs.strip()[2:])

    key = (x, y, z)
    keys.append(key)

    points_x[key] = (x, 0)
    points_y[key] = (y, 0)
    points_z[key] = (z, 0)

    initial_x[key] = (x, 0)
    initial_y[key] = (y, 0)
    initial_z[key] = (z, 0)


pairs = list(combinations(keys, 2))
step = 0

step_x = None
step_y = None
step_z = None
while True:
    points_x = apply_velocity(points_x, pairs)
    points_y = apply_velocity(points_y, pairs)
    points_z = apply_velocity(points_z, pairs)

    step += 1

    # check initial
    if step_x == None and points_x == initial_x:
        step_x = step
    if step_y == None and points_y == initial_y:
        step_y = step
    if step_z == None and points_z == initial_z:
        step_z = step

    if step_x and step_y and step_z:
        break

print(lcm(step_x, lcm(step_y, step_z)))
