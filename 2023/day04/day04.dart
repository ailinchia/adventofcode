import 'dart:io';
import 'dart:math';

Set<int> convertToSet(List<String> l) {
  Set<int> s = {};
  for (var i = 0; i < l.length; i++) {
    var n = int.tryParse(l[i]);
    if (n != null) {
      s.add(n);
    }
  }
  return s;
}

void part1(var lines) {
  var it = lines.iterator;
  num total = 0;
  while (it.moveNext()) {
    // Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    String line = it.current;
    var lineParts = line.split(":");
    var cardParts = lineParts[1].trim().split("|");
    Set<int> winningNumbers = convertToSet(cardParts[0].trim().split(" "));
    Set<int> numbers = convertToSet(cardParts[1].trim().split(" "));

    var intersection = winningNumbers.intersection(numbers);
    if (intersection.length == 0) {
      continue;
    }

    total += 1;
    for (var i = 0; i < intersection.length - 1; i++) {
      total += pow(2, i);
    }
  }

  print(total);
}

void part2(var lines) {
  var it = lines.iterator;
  num total = 0;
  Map<num, int> cardNoCount = {};
  for (var i = 0; i < lines.length; i++) {
    cardNoCount[i] = 1;
  }

  var cardNo = 0;
  while (it.moveNext()) {
    // Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    String line = it.current;
    var lineParts = line.split(":");
    var cardParts = lineParts[1].trim().split("|");
    Set<int> winningNumbers = convertToSet(cardParts[0].trim().split(" "));
    Set<int> numbers = convertToSet(cardParts[1].trim().split(" "));

    var intersection = winningNumbers.intersection(numbers);
    for (var i = 0; i < intersection.length; i++) {
      cardNoCount.update(cardNo + i + 1, (value) => value + cardNoCount[cardNo]!);
    }
    cardNo += 1;
  }

  for (var i = 0; i < cardNoCount.length; i++) {
    total += cardNoCount[i]!;
  }

  print(total);
}

void main() {
  var lines = [];
  var line;
  while ((line = stdin.readLineSync()) != null) {
    lines.add(line!);
  }

  part1(lines);
  part2(lines);
}
