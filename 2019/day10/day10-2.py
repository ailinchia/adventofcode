#!/usr/bin/env python3
import sys
import math
import operator


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


station = Point(29, 28)
# station = Point(11, 13)
# station = Point(8, 3)

y = 0
degrees = {}
for line in sys.stdin:
    for x, c in enumerate(line.strip()):
        if c == '#':
            point = Point(x, y)
            degree = math.degrees(math.atan2(point.y - station.y, point.x - station.x))
            if degree < 0:
                degree += 360

            degree += 90
            if degree >= 360:
                degree -= 360

            if degree in degrees:
                degrees[degree].append(point)
            else:
                degrees[degree] = [point]

    y += 1

for degree in sorted(degrees):
    #   0 -  90 : x asc; y desc
    if 0 <= degree <= 90:
        degrees[degree] = sorted(degrees[degree], key=lambda p: (p.x, -p.y))
        pass
    #  90 - 180 : x asc; y asc
    elif 90 < degree <= 180:
        degrees[degree] = sorted(degrees[degree], key=lambda p: (p.x, p.y))
        pass
    # 180 - 270 : x desc; y asc
    elif 180 < degree <= 270:
        degrees[degree] = sorted(degrees[degree], key=lambda p: (-p.x, p.y))
        pass
    # 270 - 360 : x desc; y desc
    elif 270 < degree <= 360:
        degrees[degree] = sorted(degrees[degree], key=lambda p: (-p.x, -p.y))

i = 0
while True:
    for degree in sorted(degrees):
        i += 1
        point = degrees[degree].pop(0)
        if len(degrees[degree]) == 0:
            del degrees[degree]

        # print(i, degree, point)
        if i == 200:
            print(point.x * 100 + point.y)
            quit()

    if len(degrees) == 0:
        break
