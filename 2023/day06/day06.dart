import 'dart:io';

void part1(List<String> lines) {
  var time = lines[0].split(":")[1].trim().split(RegExp(r'\s+')).map((e) => int.parse(e)).toList();
  var distance = lines[1].split(":")[1].trim().split(RegExp(r'\s+')).map((e) => int.parse(e)).toList();

  var total = 1;
  for (var i = 0; i < time.length; i++) {
    var t = time[i];
    var d = distance[i];

    var count = 0;
    for(var b = 1; b <= t; b++) {
      var distance = (t - b) * b;
      if (distance > d) {
        // print("t: $t, d: $d, b: $b");
        count += 1;
      }
    }

    total *= count;
    // distance = (time - buttonPress) * buttonPress

  }
  print(total);
}

void part2(List<String> lines) {
  var time = lines[0].split(":")[1].trim().replaceAll(' ', '');
  var duration = lines[1].split(":")[1].trim().replaceAll(' ', '');

  var count = 0;
  var t = int.parse(time);
  var d = int.parse(duration);
  for(var b = 1; b <= t; b++) {
    var distance = (t - b) * b;
    if (distance > d) {
      count += 1;
    }
  }

  print(count);
}

/*
Time:      7  15   30
Distance:  9  40  200
 */
void main() {
  List<String> lines = [];
  var line;
  while ((line = stdin.readLineSync()) != null) {
    lines.add(line!);
  }

  part1(lines);
  part2(lines);
}
