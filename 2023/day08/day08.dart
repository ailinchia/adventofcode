import 'dart:io';

void part1(String instructions, Map<String, NetworkNode> map) {
  String current = 'AAA';
  int steps = 0;
  // print(map);
  while (true) {
    for (var c in instructions.split('')) {
      // print(current);
      current = map[current]!.getNode(c);
      steps += 1;
      if (current == 'ZZZ') {
        print(steps);
        return;
      }
    }
  }
}

int gcd(int a, int b) {
  while (b != 0) {
    var t = b;
    b = a % t;
    a = t;
  }
  return a;
}

int lcm(int a, int b) => (a * b) ~/ gcd(a, b);

void part2(String instructions, Map<String, NetworkNode> map) {
  // get all nodes that ends with A
  List<String> nodes = map.keys.where((element) => element.endsWith('A')).toList();

  List<int> allSteps = [];
  for (var n in nodes) {
    String current = n;
    int steps = 0;
    while (true) {
      for (var c in instructions.split('')) {
        current = map[current]!.getNode(c);
        steps += 1;
        if (current.endsWith('Z')) {
          allSteps.add(steps);
          break;
        }
      }
      if (current.endsWith('Z')) {
        break;
      }
    }
  }

  // get LCM for allSteps
  var a = lcm(allSteps[0], allSteps[1]);
  for (var i = 2; i < allSteps.length; i++) {
    a = lcm(a, allSteps[i]);
  }
  print(a);
}

class NetworkNode {
  NetworkNode(this.left, this.right);

  String getNode(String side) {
    return side == 'L' ? left : right;
  }

  @override
  String toString() {
    return '($left, $right)';
  }
  String left;
  String right;
}

void main() {
  Map<String, NetworkNode> map = {};
  String instructions = stdin.readLineSync()!;

  var line;
  while ((line = stdin.readLineSync()) != null) {
    if (line.isEmpty) {
      continue;
    }

    String l = line.replaceAll(RegExp(r'([(,)])|( =)'), '');
    // print(l);
    var parts = l.split(' ');
    map[parts[0]] = NetworkNode(parts[1], parts[2]);
  }

  part1(instructions, map);
  part2(instructions, map);
}
