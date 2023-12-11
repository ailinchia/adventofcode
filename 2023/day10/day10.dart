import 'dart:io';

class Point {
  int x;
  int y;
  String c;

  Point(this.x, this.y, this.c);
  Point.empty() : x = -1, y = -1, c = "";

  bool isEmpty() {
    return x == -1 && y == -1 && c == "";
  }

  @override
  String toString() {
    return "Point($x, $y, $c)";
  }

  @override
  bool operator ==(Object other) {
    if (other is Point) {
      return x == other.x && y == other.y && c == other.c;
    }
    return false;
  }
}

void getNeighbourUp(List<Point> n, Point p, List<String> lines) {
  if (p.y > 0) {
    var c = lines[p.y - 1][p.x];
    if (c != '.') {
      var pn = Point(p.x, p.y - 1, c);
      if (!n.contains(pn)) {
        n.add(pn);
      }
    }
  }
}

void getNeighbourDown(List<Point> n, Point p, List<String> lines) {
  if (p.y < lines.length - 1) {
    var c = lines[p.y + 1][p.x];
    if (c != '.') {
      var pn = Point(p.x, p.y + 1, c);
      if (!n.contains(pn)) {
        n.add(pn);
      }
    }
  }
}

void getNeighbourLeft(List<Point> n, Point p, List<String> lines) {
  if (p.x > 0) {
    var c = lines[p.y][p.x - 1];
    if (c != '.') {
      var pn = Point(p.x - 1, p.y, c);
      if (!n.contains(pn)) {
        n.add(pn);
      }
    }
  }
}

void getNeighbourRight(List<Point> n, Point p, List<String> lines) {
  if (p.x < lines[p.y].length - 1) {
    var c = lines[p.y][p.x + 1];
    if (c != '.') {
      var pn = Point(p.x + 1, p.y, c);
      if (!n.contains(pn)) {
        n.add(pn);
      }
    }
  }
}

/*
The pipes are arranged in a two-dimensional grid of tiles:
  | is a vertical pipe connecting north and south.
  - is a horizontal pipe connecting east and west.
  L is a 90-degree bend connecting north and east.
  J is a 90-degree bend connecting north and west.
  7 is a 90-degree bend connecting south and west.
  F is a 90-degree bend connecting south and east.
  . is ground; there is no pipe in this tile.
  S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
 */

List<Point> getNeighbour(int x, int y, List<String> lines) {
  List<Point> neighbours = [];
  var p = Point(x, y, lines[y][x]);
  switch (p.c) {
    case '|':
      getNeighbourUp(neighbours, p, lines);
      getNeighbourDown(neighbours, p, lines);
      break;
    case '-':
      getNeighbourLeft(neighbours, p, lines);
      getNeighbourRight(neighbours, p, lines);
      break;
    case 'L':
      getNeighbourUp(neighbours, p, lines);
      getNeighbourRight(neighbours, p, lines);
      break;
    case 'J':
      getNeighbourUp(neighbours, p, lines);
      getNeighbourLeft(neighbours, p, lines);
      break;
    case '7':
      getNeighbourDown(neighbours, p, lines);
      getNeighbourLeft(neighbours, p, lines);
      break;
    case 'F':
      getNeighbourDown(neighbours, p, lines);
      getNeighbourRight(neighbours, p, lines);
      break;
    case 'S':
      getNeighbourUp(neighbours, p, lines);
      getNeighbourDown(neighbours, p, lines);
      // getNeighbourLeft(neighbours, p, lines);
      // getNeighbourRight(neighbours, p, lines);
      break;
  }

  return neighbours;
}

// void findPath(List<Point> paths, List<Point> neighbours, Point p, List<String> lines) {
//   // print("findPath: $paths");
//   // print("findPath: $p");
//   paths.add(p);
//
//   for (var n in neighbours) {
//     if (paths.contains(n)) {
//       continue;
//     }
//     // print(n);
//     findPath(paths, getNeighbour(n.x, n.y, lines), n, lines);
//   }
// }

void part1(List<String> lines) {
  var startX = -1;
  var startY = -1;
  for (var line in lines) {
    startY += 1;
    if (line.indexOf('S') != -1) {
      startX = line.indexOf('S');
      break;
    }
  }

  Point s = Point(startX, startY, 'S');
  List<Point> paths = [s];
  Set<Point> neighbours = getNeighbour(s.x, s.y, lines).toSet();

  while (neighbours.isNotEmpty) {
    var n = neighbours.first;
    neighbours.remove(n);
    if (paths.contains(n)) {
      continue;
    }
    // print(n);
    paths.add(n);
    neighbours.addAll(getNeighbour(n.x, n.y, lines));
  }

  print(paths.length / 2);
}

void part2(List<String> lines) {
  var startX = -1;
  var startY = -1;
  for (var line in lines) {
    startY += 1;
    if (line.indexOf('S') != -1) {
      startX = line.indexOf('S');
      break;
    }
  }

  Point s = Point(startX, startY, 'S');
  List<Point> paths = [s];
  Set<Point> neighbours = getNeighbour(s.x, s.y, lines).toSet();

  while (neighbours.isNotEmpty) {
    var n = neighbours.first;
    neighbours.remove(n);
    if (paths.contains(n)) {
      continue;
    }
    paths.add(n);
    neighbours.addAll(getNeighbour(n.x, n.y, lines));
  }

  // print(paths);
  for (var y = 0; y < lines.length; y++) {
    for (var x = 0; x < lines[y].length; x++) {
      if (lines[y][x] == '.') {
        continue;
      }

      Point p = Point(x, y, lines[y][x]);
      if (paths.contains(p)) {
        continue;
      }
      // print(p);
      lines[y] = lines[y].replaceRange(x, x+1, '.');
    }
  }

  // remove dots from start
  for (var y = 0; y < lines.length; y++) {
    for (var x = 0; x < lines[y].length; x++) {
      if (lines[y][x] == '.') {
        lines[y] = lines[y].replaceRange(x, x+1, ' ');
        continue;
      }

      break;
    }
  }

  // remove dots from end
  for (var y = lines.length - 1; y >= 0; y--) {
    for (var x = lines[y].length - 1; x >= 0; x--) {
      if (lines[y][x] == '.') {
        lines[y] = lines[y].replaceRange(x, x+1, ' ');
        continue;
      }

      break;
    }
  }

  for (var line in lines) {
    line = line.replaceAll('F', '┌').replaceAll('7', '┐').replaceAll('J', '┘').replaceAll('L', '└').replaceAll('|', '│').replaceAll('-', '─');
    print(line);
  }

  // TODO: Add programming solution instead of manual solution
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
