import 'dart:io';
import "package:trotter/trotter.dart";

class Point {
  int x;
  int y;

  Point(this.x, this.y);

  @override
  String toString() {
    return "Point($x, $y)";
  }

  @override
  bool operator ==(Object other) {
    if (other is Point) {
      return x == other.x && y == other.y;
    }
    return false;
  }
}

int getTotalLength(List<String> lines, int expand) {
  List<int> allEmptyX = [];
  for (var x = 0; x < lines[0].length; x++) {
    var allEmpty = true;
    for (var y = 0; y < lines.length; y++) {
      if (lines[y][x] != '.') {
        allEmpty = false;
        break;
      }
    }
    if (allEmpty) {
      allEmptyX.add(x);
    }
  }

  List<int> allEmptyY = [];
  for (var y = 0; y < lines.length; y++) {
    if (lines[y].split('').every((element) => element == '.')) {
      allEmptyY.add(y);
    }
  }

  // get galaxy
  List<Point> galaxies = [];
  for (var y = 0; y < lines.length; y++) {
    for (var x = 0; x < lines[y].length; x++) {
      if (lines[y][x] == '#') {
        galaxies.add(Point(x, y));
      }
    }
  }

  // expand universe
  if (expand > 1) {
    expand -= 1;
  }

  for (var i = allEmptyX.length - 1; i >= 0; i--) {
    var x = allEmptyX[i];
    for (var j = 0; j < galaxies.length; j++) {
      if (galaxies[j].x > x) {
        galaxies[j].x += expand;
      }
    }
  }
  for (var i = allEmptyY.length - 1; i >= 0; i--) {
    var y = allEmptyY[i];
    for (var j = 0; j < galaxies.length; j++) {
      if (galaxies[j].y > y) {
        galaxies[j].y += expand;
      }
    }
  }

  var pointPairs = Combinations(2, galaxies);

  int total = 0;

  // get steps for each pair
  for (var pp in pointPairs()) {
    var dx = (pp[1].x - pp[0].x).abs();
    var dy = (pp[1].y - pp[0].y).abs();
    var steps = dx + dy;
    // print("pp: $pp dx: $dx, dy: $dy steps: $steps");
    total += steps;
  }
  return total;
}

void part1(List<String> lines) {
  print(getTotalLength(lines, 1));
}

void part2(List<String> lines) {
  print(getTotalLength(lines, 1000000));
}

void main() {
  List<String> lines = [];
  var line;
  while ((line = stdin.readLineSync()) != null) {
    lines.add(line!);
  }

  part1(lines);
  part2(lines);
}
