#!/usr/bin/env python3
import sys

reactions = {}
for line in sys.stdin:
    inputs_str, output_str = line.strip().split('=>')
    output = output_str.strip().split(' ')

    inputs = [i.strip().split(' ') for i in inputs_str.strip().split(',')]
    inputs = [(int(x), y) for x, y in inputs]

    reactions[output[1]] = (int(output[0]), inputs)

extras = {}
for reaction in reactions:
    extras[reaction] = 0

reaction_count, reaction = reactions['FUEL']
while len(reaction) != 1:
    output = []
    ore_count = 0
    for (need_count, i) in reaction:
        if i == 'ORE':
            ore_count += need_count
            continue

        # consume extras
        extra_count = extras[i]
        if extra_count > 0:
            min_count = min(extra_count, need_count)
            need_count -= min_count
            extra_count -= min_count
            extras[i] = extra_count

        if need_count > 0:
            has_count, input_chems = reactions[i]
            multiples = 1
            while (has_count * multiples) // need_count == 0:
                multiples += 1
            extra_count = (has_count * multiples) - need_count
            extras[i] += extra_count
            for m in range(multiples):
                output += [c for c in input_chems]

    if ore_count > 0:
        output.append((ore_count, 'ORE'))

    reaction = output

print(output[0][0])
