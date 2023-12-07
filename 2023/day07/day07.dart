import 'dart:io';

/*
Every hand is exactly one type. From strongest to weakest, they are:
  Five of a kind, where all five cards have the same label: AAAAA
  Four of a kind, where four cards have the same label and one card has a different label: AA8AA
  Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
  Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
  Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
  One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
  High card, where all cards' labels are distinct: 23456
 */
const List<String> cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'];
const List<String> cards2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'];

class Hand {
  List<String> hand;
  Set<String> set;
  bool useJoker = false;

  Hand(this.hand, this.useJoker)
    : set = hand.toSet() {
  }

  bool hasJoker() {
    return useJoker && set.contains('J');
  }

  int jokerCount() {
    return hand.where((element) => element == 'J').length;
  }

  bool isFiveOfAKind() {
    return set.length == 1 || (set.length == 2 && hasJoker());
  }

  bool isFourOfAKind() {
    if (hasJoker()) {
      return set.length == 3 && set.any((element) => element != 'J' && hand.where((e) => e == element).length == 4 - jokerCount());
    }
    return (set.length == 2 && set.any((element) => hand.where((e) => e == element).length == 4));
  }

  bool isFullHouse() {
    if (hasJoker()) {
      return (set.length == 3 && set.any((element) => element != 'J' && hand.where((e) => e == element).length == 3 - jokerCount()));
    }
    return set.length == 2 && set.any((element) => hand.where((e) => e == element).length == 3);
  }

  bool isThreeOfAKind() {
    if (hasJoker()) {
      return (set.length == 4 && set.any((element) => element != 'J' && hand.where((e) => e == element).length == 3 - jokerCount()));
    }
    return set.length == 3 && (hand.where((element) => element == set.elementAt(0)).length == 3 || hand.where((element) => element == set.elementAt(1)).length == 3 || hand.where((element) => element == set.elementAt(2)).length == 3);
  }

  bool isTwoPair() {
    if (hasJoker()) {
      return (set.length == 4 && set.any((element) => element != 'J' && hand.where((e) => e == element).length == 2 - jokerCount()));
    }
    return set.length == 3 && (hand.where((element) => element == set.elementAt(0)).length == 2 || hand.where((element) => element == set.elementAt(1)).length == 2 || hand.where((element) => element == set.elementAt(2)).length == 2);
  }

  bool isOnePair() {
    if (hasJoker()) {
      return set.length == 5;
    }
    return set.length == 4;
  }

  bool isHighCard() {
    return set.length == 5;
  }

  int compareTo(Hand other) {
    for (var i = 0; i < hand.length; i++) {
      var a = hand[i];
      var b = other.hand[i];
      var c = useJoker ? cards2 : cards;
      if (c.indexOf(a) > c.indexOf(b)) {
        return -1;
      } else if (c.indexOf(a) < c.indexOf(b)) {
        return 1;
      }
    }
    return 0;
  }

  @override
  String toString() {
    return hand.join('');
  }
}

int compare(Hand a, Hand b) {
  if (a.isFiveOfAKind() || b.isFiveOfAKind()) {
    if (a.isFiveOfAKind() == b.isFiveOfAKind()) {
      return a.compareTo(b);
    }
    return a.isFiveOfAKind() ? 1: -1;
  } else if (a.isFourOfAKind() || b.isFourOfAKind()) {
    if (a.isFourOfAKind() == b.isFourOfAKind()) {
      return a.compareTo(b);
    }
    return a.isFourOfAKind() ? 1: -1;
  } else if (a.isFullHouse() || b.isFullHouse()) {
    if (a.isFullHouse() == b.isFullHouse()) {
      return a.compareTo(b);
    }
    return a.isFullHouse() ? 1 : -1;
  } else if (a.isThreeOfAKind() || b.isThreeOfAKind()) {
    if (a.isThreeOfAKind() == b.isThreeOfAKind()) {
      return a.compareTo(b);
    }
    return a.isThreeOfAKind() ? 1 : -1;
  } else if (a.isTwoPair() || b.isTwoPair()) {
    if (a.isTwoPair() == b.isTwoPair()) {
      return a.compareTo(b);
    }
    return a.isTwoPair() ? 1 : -1;
  } else if (a.isOnePair() || b.isOnePair()) {
    if (a.isOnePair() == b.isOnePair()) {
      return a.compareTo(b);
    }
    return a.isOnePair() ? 1 : -1;
  } else if (a.isHighCard() || b.isHighCard()) {
    if (a.isHighCard() == b.isHighCard()) {
      return a.compareTo(b);
    }
    return a.isHighCard() ? 1 : -1;
  }
  return 0;
}

void part1(Map<String, int> map) {
  List<Hand> hands = map.keys.toList().map((e) => Hand(e.split(''), false)).toList();
  hands.sort(compare);

  var total = 0;
  for (var i = 0; i < hands.length; i++) {
    total += (map[hands[i].toString()]! * (i + 1));
  }
  print(total);
}

// 248367180 too low
void part2(Map<String, int> map) {
  List<Hand> hands = map.keys.toList().map((e) => Hand(e.split(''), true)).toList();
  hands.sort(compare);

  var total = 0;
  for (var i = 0; i < hands.length; i++) {
    total += (map[hands[i].toString()]! * (i + 1));
  }
  print(total);
}

void main() {
  Map<String, int> map = {};
  var line;
  while ((line = stdin.readLineSync()) != null) {
    var lineParts = line.split(' ');
    map[lineParts[0]] = int.parse(lineParts[1]);
  }

  part1(map);
  part2(map);
}
