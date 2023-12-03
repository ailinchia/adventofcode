import 'dart:io';

// 538756 too high
// 538226 too high
// 538123 too high
// 428693 wrong answer
void part1(var lines) {
  var it = lines.iterator;
  var total = 0;
  List<String> grids = [];
  Set<String> symbols = {};

  while (it.moveNext()) {
    grids.add(it.current);

    String s = it.current.replaceAll(RegExp(r'[\d.]'), '');
    for (var i = 0; i < s.length; i++) {
      symbols.add(s[i]);
    }
  }

  String symbolsAll = "[.";
  for (var s in symbols) {
    if (s == "-") {
      symbolsAll += "\\";
    }
    symbolsAll += s;
  }
  symbolsAll += "]";

  List<Set<String>> partNos = [];
  for (var i = 0; i < grids.length; i++) {
    Set<String> currentPartNos = {};
    var currentLine = grids[i];

    currentLine = currentLine.replaceAll(RegExp(symbolsAll), ".");

    var lineParts = currentLine.split(".");
    for (var j = 0; j < lineParts.length; j++) {
      if (lineParts[j] == "") {
        continue;
      }

      currentPartNos.add(lineParts[j]);
      // print(lineParts[j]);
    }
    partNos.add(currentPartNos);
    // print("-----");
    // print(grids[i]);
  }
  // print(partNos);

  for (var i = 0; i < grids.length; i++) {
    var currentLine = grids[i];
    var currentPartNos = partNos[i];

    // print("currentPartNos: $currentPartNos");
    // print("-----");
    // if (i > 0) {
    //   print(grids[i - 1]);
    // }
    // print(currentLine);
    // if (i < grids.length - 1) {
    //   print(grids[i + 1]);
    // }
    // print("-----");

    for (var j = 0; j < currentPartNos.length; j++) {
      var currentPartNo = currentPartNos.elementAt(j);
      var posStart = -1;
      var exp = RegExp("(?<mid>${symbolsAll + currentPartNo + symbolsAll})|(?<start>^${currentPartNo + symbolsAll})|(?<end>${symbolsAll + currentPartNo}\$)");

      var matches = exp.allMatches(currentLine);
      for (var m in matches) {
        if (m.namedGroup("mid") != null || m.namedGroup("end") != null) {
          posStart = m.start + 1;
        } else if (m.namedGroup("start") != null) {
          posStart = 0;
        }

        var posEnd = posStart + currentPartNo.length;

        // check left
        if (posStart > 0) {
          if (symbols.contains(currentLine[posStart - 1])) {
            // valid part no
            // print("l[${posStart - 1}] - ${currentPartNo} ${currentLine[posStart - 1]}");
            total += int.parse(currentPartNo);
            continue;
          }
        }

        // check right
        if (posEnd < currentLine.length) {
          // print("= ${currentPartNo} ${currentLine[posEnd-1]} ${currentLine[posEnd]}");
          if (symbols.contains(currentLine[posEnd])) {
            // valid part no
            // print("r[${posEnd}] - ${currentPartNo} ${currentLine[posEnd]}");
            total += int.parse(currentPartNo);
            continue;
          }
        }

        // check up
        if (i > 0) {
          var upLine = grids[i - 1];
          var upLineStart = posStart;
          if (upLineStart > 0) {
            upLineStart -= 1;
          }
          var upLineEnd = posEnd;
          if (upLineEnd < upLine.length) {
            upLineEnd += 1;
          }

          // print("u - ${currentPartNo} ${upLine[upLineStart]} ${upLineStart} ${upLineEnd}");
          bool valid = false;
          for (var k = upLineStart; k < upLineEnd; k++) {
            if (symbols.contains(upLine[k])) {
              // valid part no
              // print("u[${k}] - ${currentPartNo} ${upLine[k]}");
              total += int.parse(currentPartNo);
              valid = true;
              break;
            }
          }
          if (valid) {
            continue;
          }
        }

        // check down
        if (i < grids.length - 1) {
          var downLine = grids[i + 1];
          var downLineStart = posStart;
          if (downLineStart > 0) {
            downLineStart -= 1;
          }
          var downLineEnd = posEnd;
          if (downLineEnd < downLine.length) {
            downLineEnd += 1;
          }

          bool valid = false;
          for (var k = downLineStart; k < downLineEnd; k++) {
            if (symbols.contains(downLine[k])) {
              // valid part no
              // print("d[${k}] - ${currentPartNo} ${downLine[k]}");
              total += int.parse(currentPartNo);
              valid = true;
              break;
            }
          }
          if (valid) {
            continue;
          }
        }
      }
    }
  }
  print(total);
}

void part2(var lines) {
  var it = lines.iterator;
  var total = 0;
  List<String> grids = [];
  Set<String> symbols = {};

  while (it.moveNext()) {
    grids.add(it.current);

    String s = it.current.replaceAll(RegExp(r'[\d.]'), '');
    for (var i = 0; i < s.length; i++) {
      symbols.add(s[i]);
    }
  }

  String symbolsAll = "[.";
  for (var s in symbols) {
    if (s == "-") {
      symbolsAll += "\\";
    }
    symbolsAll += s;
  }
  symbolsAll += "]";

  List<Set<String>> partNos = [];
  for (var i = 0; i < grids.length; i++) {
    Set<String> currentPartNos = {};
    var currentLine = grids[i];

    currentLine = currentLine.replaceAll(RegExp(symbolsAll), ".");

    var lineParts = currentLine.split(".");
    for (var j = 0; j < lineParts.length; j++) {
      if (lineParts[j] == "") {
        continue;
      }

      currentPartNos.add(lineParts[j]);
    }
    partNos.add(currentPartNos);
  }

  Map<String, List<int>> partNoMap = {};
  for (var i = 0; i < grids.length; i++) {
    var currentLine = grids[i];
    var currentPartNos = partNos[i];

    for (var j = 0; j < currentPartNos.length; j++) {
      var currentPartNo = currentPartNos.elementAt(j);
      var posStart = -1;
      var exp = RegExp("(?<mid>${symbolsAll + currentPartNo + symbolsAll})|(?<start>^${currentPartNo + symbolsAll})|(?<end>${symbolsAll + currentPartNo}\$)");

      var matches = exp.allMatches(currentLine);
      for (var m in matches) {
        if (m.namedGroup("mid") != null || m.namedGroup("end") != null) {
          posStart = m.start + 1;
        } else if (m.namedGroup("start") != null) {
          posStart = 0;
        }

        var posEnd = posStart + currentPartNo.length;

        // check left
        if (posStart > 0) {
          if (currentLine[posStart - 1] == "*") {
            var l = partNoMap["${i}_${posStart - 1}"];
            if (l == null) {
              l = [];
            }
            l.add(int.parse(currentPartNo));
            partNoMap["${i}_${posStart - 1}"] = l;
          }
        }

        // check right
        if (posEnd < currentLine.length) {
          if (currentLine[posEnd] == "*") {
            var l = partNoMap["${i}_${posEnd}"];
            if (l == null) {
              l = [];
            }
            l.add(int.parse(currentPartNo));
            partNoMap["${i}_${posEnd}"] = l;
          }
        }

        // check up
        if (i > 0) {
          var upLine = grids[i - 1];
          var upLineStart = posStart;
          if (upLineStart > 0) {
            upLineStart -= 1;
          }
          var upLineEnd = posEnd;
          if (upLineEnd < upLine.length) {
            upLineEnd += 1;
          }

          for (var k = upLineStart; k < upLineEnd; k++) {
            if (symbols.contains(upLine[k])) {
              // valid part no
              if (upLine[k] == "*") {
                var l = partNoMap["${i - 1}_${k}"];
                if (l == null) {
                  l = [];
                }
                l.add(int.parse(currentPartNo));
                partNoMap["${i - 1}_${k}"] = l;
              }
            }
          }
        }

        // check down
        if (i < grids.length - 1) {
          var downLine = grids[i + 1];
          var downLineStart = posStart;
          if (downLineStart > 0) {
            downLineStart -= 1;
          }
          var downLineEnd = posEnd;
          if (downLineEnd < downLine.length) {
            downLineEnd += 1;
          }

          for (var k = downLineStart; k < downLineEnd; k++) {
            if (symbols.contains(downLine[k])) {
              // valid part no
              if (downLine[k] == "*") {
                var l = partNoMap["${i + 1}_${k}"];
                if (l == null) {
                  l = [];
                }
                l.add(int.parse(currentPartNo));
                partNoMap["${i + 1}_${k}"] = l;
              }
            }
          }
        }
      }
    }
  }
  for (var pIt in partNoMap.entries) {
    if (pIt.value.length == 2) {
      total += (pIt.value[0] * pIt.value[1]);
    }
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
