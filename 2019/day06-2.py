#!/usr/bin/env python3
import sys


# function to find the shortest path
def find_shortest_path(graph, start, end, path =[]):
    path = path + [start]
    if start == end:
        return path
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

orbits = {}
for line in sys.stdin:
    (object0, object1) = line.strip().split(')')    
    arr0 = orbits.get(object0, [])
    arr0.append(object1)
    orbits[object0] = arr0
    arr1 = orbits.get(object1, [])
    arr1.append(object0)
    orbits[object1] = arr1



shortest = find_shortest_path(orbits, 'YOU', 'SAN')
print(len(shortest)-3)
