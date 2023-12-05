import 'dart:io';

const List<String> maps = [
  "seed-to-soil",
  "soil-to-fertilizer",
  "fertilizer-to-water",
  "water-to-light",
  "light-to-temperature",
  "temperature-to-humidity",
  "humidity-to-location",
];

const destRangeStartPos = 0;
const sourceRangeStartPos = 1;
const rangeLengthPos = 2;

void part1(var lines) {
  List<int> seeds = lines["seeds"][0];
  var lowestLocation = -1;

  for (var seed in seeds) {
    var result = seed;
    for (var m in maps) {
      var l = lines[m];
      for (var i = 0; i < l.length; i++) {
        var range = l[i];
        if (result >= range[sourceRangeStartPos] && result < range[sourceRangeStartPos] + range[rangeLengthPos]) {
          result = range[destRangeStartPos] + (result - range[sourceRangeStartPos]);
          break;
        }
      }
    }
    if (lowestLocation == -1 || result < lowestLocation) {
      lowestLocation = result;
    }
  }
  print(lowestLocation);
}

// 20283861 too high
void part2(var lines) {
  List<int> seeds = lines["seeds"][0];
  var lowestLocation = -1;

  for (var i = 0; i < seeds.length; i+=2) {
    print("${seeds[i]} - ${seeds[i + 1]}");
    var seed = seeds[i];
    for (var j = 0; j < seeds[i + 1]; j++) {
      var result = seed + j;
      // print(result);
      for (var m in maps) {
        var l = lines[m];
        for (var i = 0; i < l.length; i++) {
          var range = l[i];
          if (result >= range[sourceRangeStartPos] && result < range[sourceRangeStartPos] + range[rangeLengthPos]) {
            result = range[destRangeStartPos] + (result - range[sourceRangeStartPos]);
            break;
          }
        }
      }
      if (lowestLocation == -1 || result < lowestLocation) {
        lowestLocation = result;
      }
    }
  }

  print(lowestLocation);
}

void main() {
  Map<String, List<List<int>>> lines = {};
  String? line;

  var currentKey = "";
  while ((line = stdin.readLineSync()) != null) {
    if (line!.trim().length == 0) {
      continue;
    }

    if (line.startsWith("seeds")) {
      lines["seeds"] = [line.split(":")[1].trim().split(" ").map((e) => int.parse(e)).toList()];
      continue;
    } else if (line.endsWith(" map:")) {
      currentKey = line.split(" ")[0].trim();
      lines[currentKey] = [];
      continue;
    }

    // print("===" + currentKey);
    lines[currentKey]!.add(line.trim().split(" ").map((e) => int.parse(e)).toList());
  }

  part1(lines);
  part2(lines);
}
