import 'dart:io';

void part1(var lines) {
  // only 12 red cubes, 13 green cubes, and 14 blue cubes
  final maxRed = 12;
  final maxGreen = 13;
  final maxBlue = 14;

  var it = lines.iterator;
  var total = 0;
  var gameNo = 1;
  while (it.moveNext()) {
    // Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    bool possible = true;
    String line = it.current;
    var lineParts = line.split(":");
    var cubeParts  = lineParts[1].trim().split(";");
    for (var cubePart in cubeParts) {
      var setParts = cubePart.trim().split(",");
      for (var setPart in setParts) {
        var setPartParts = setPart.trim().split(" ");
        var color = setPartParts[1];
        var count = int.parse(setPartParts[0]);

        switch (color) {
          case "red":
            if (count > maxRed) {
              possible = false;
            }
            break;
          case "green":
            if (count > maxGreen) {
              possible = false;
            }
            break;
          case "blue":
            if (count > maxBlue) {
              possible = false;
            }
            break;
        }

        if (!possible) {
          break;
        }
      }
      if (!possible) {
        break;
      }
    }

    if (possible) {
      total += gameNo;
    }
    gameNo += 1;
  }

  print(total);
}

void part2(var lines) {
  var it = lines.iterator;
  var total = 0;
  while (it.moveNext()) {
    int maxRed = 0;
    int maxGreen = 0;
    int maxBlue = 0;

    // Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    String line = it.current;
    var lineParts = line.split(":");
    var cubeParts  = lineParts[1].trim().split(";");
    for (var cubePart in cubeParts) {
      var setParts = cubePart.trim().split(",");
      for (var setPart in setParts) {
        var setPartParts = setPart.trim().split(" ");
        var color = setPartParts[1];
        var count = int.parse(setPartParts[0]);

        switch (color) {
          case "red":
            if (count > maxRed) {
              maxRed = count;
            }
            break;
          case "green":
            if (count > maxGreen) {
              maxGreen = count;
            }
            break;
          case "blue":
            if (count > maxBlue) {
              maxBlue = count;
            }
            break;
        }
      }
    }

    total += (maxRed * maxGreen * maxBlue);
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
