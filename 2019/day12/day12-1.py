#!/usr/bin/env python3
import sys
from itertools import combinations


def get_velocity(p0, p1):
    if p0 == p1:
        return 0
    elif p0 > p1:
        return -1
    else:
        return 1


class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Point3D(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'

    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash(str(self.x) + '_' + str(self.y) + '_' + str(self.z))

    def get_velocity(self, other):
        return Point3D(get_velocity(self.x, other.x), get_velocity(self.y, other.y), get_velocity(self.z, other.z))


points = {}
for line in sys.stdin:
    xs, ys, zs = line.strip()[1:-1].split(',')
    point = Point3D(int(xs.strip()[2:]), int(ys.strip()[2:]), int(zs.strip()[2:]))
    key = Point3D(point.x, point.y, point.z)
    points[key] = point

pairs = list(combinations(points.keys(), 2))
velocities = {}
for ts in range(0, 1000):
    # calculate velocity
    for i, (k0, k1) in enumerate(pairs):
        m0 = points[k0]
        m1 = points[k1]

        m0v = m0.get_velocity(m1)
        if k0 in velocities:
            velocities[k0] += m0v
        else:
            velocities[k0] = m0v

        m1v = m1.get_velocity(m0)
        if k1 in velocities:
            velocities[k1] += m1v
        else:
            velocities[k1] = m1v

    # apply velocity
    for key in velocities:
        points[key] += velocities[key]

# calculate energy
total_energy = 0
for key in points:
    p0 = points[key]
    p1 = velocities[key]
    total_energy += ((abs(p0.x) + abs(p0.y) + abs(p0.z)) * (abs(p1.x) + abs(p1.y) + abs(p1.z)))

print(total_energy)
