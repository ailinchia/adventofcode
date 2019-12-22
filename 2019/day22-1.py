#!/usr/bin/env python3
import sys

card_count = 10007
#card_count = 10
cards = [i for i in range(card_count)]
for line in sys.stdin:
    line = line.strip()
    if line == "deal into new stack":
        cards.reverse()
    elif line.startswith("cut "):
        cut = int(line[len("cut "):])
        cards = cards[cut:] + cards[:cut]
    elif line.startswith("deal with increment "):
        increment = int(line[len("deal with increment "):])
        new_cards = [-1 for i in range(card_count)]

        i = 0
        while len(cards) > 0:
            c = cards.pop(0)
            new_cards[i] = c
            i += increment
            i %= card_count
        cards = new_cards
print(cards.index(2019))
