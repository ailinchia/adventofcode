import 'dart:io';

void part1(var lines) {
  var it = lines.iterator;
  var total = 0;
  while (it.moveNext()) {
    var line = it.current;
    var first = line.indexOf(RegExp(r'\d'));
    var last = it.current.lastIndexOf(RegExp(r'\d'));

    if (first == -1 || last == -1) {
      continue;
    }

    total += int.parse(line[first] + line[last]);
  }

  print(total);
}

void part2(var lines) {
  const numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"];
  var it = lines.iterator;
  int total = 0;
  while (it.moveNext()) {
    var line = it.current;

    var firstLetterPos = line.indexOf(RegExp(r'\d'));
    int firstDigit = 0;
    if (firstLetterPos != -1) {
      firstDigit = int.parse(line[firstLetterPos]);
    }

    var lastLetterPos = it.current.lastIndexOf(RegExp(r'\d'));
    int lastDigit = 0;
    if (lastLetterPos != -1) {
      lastDigit = int.parse(line[lastLetterPos]);
    }

    for (var i = 0; i < numbers.length; i++) {
      var pos = line.indexOf(numbers[i]);
      if (pos != -1 && (firstLetterPos == -1 || pos < firstLetterPos)) {
        firstLetterPos = pos;
        firstDigit = i + 1;
      }
      pos = line.lastIndexOf(numbers[i]);
      if (pos != -1 && (lastLetterPos == -1 || pos > lastLetterPos)) {
        lastLetterPos = pos;
        lastDigit = i + 1;
      }
    }

    total += (firstDigit * 10) + lastDigit;
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
