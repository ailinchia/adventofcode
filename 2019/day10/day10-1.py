#!/usr/bin/env python3
import sys


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point(' + str(self.x) + ', ' + str(self.y) + ')'


def is_on(a, b, c):
    "Return true if point c intersects the line segment from a to b."
    # (or the degenerate case that all 3 points are coincident)
    return ((within(a.x, c.x, b.x) if a.x != b.x else within(a.y, c.y, b.y)) and collinear(a, b, c))


def collinear(a, b, c):
    "Return true if a, b, and c all lie on the same line."
    return (b.x - a.x) * (c.y - a.y) == (c.x - a.x) * (b.y - a.y)


def within(p, q, r):
    "Return true if q is between p and r (inclusive)."
    return p <= q <= r or r <= q <= p


y = 0
points = []
for line in sys.stdin:
    for x, c in enumerate(line.strip()):
        if c == '#':
            points.append(Point(x, y))
    y += 1

max_count = 0
for point_start in points:
    point_on_line = False
    count = 0

    for point_end in points:
        if point_start == point_end:
            continue

        for point in points:
            if point_start == point or point_end == point:
                continue

            point_on_line = is_on(point_start, point_end, point)
            if point_on_line:
                break

        if not point_on_line:
            count += 1

    if count > max_count:
        max_count = count
        max_count_point = point_start
print(max_count, max_count_point)
