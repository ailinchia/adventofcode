import 'dart:convert';
import 'dart:io';

void part1(List<List<int>> report) {
  int total = 0;
  for (var values in report) {
    List<List<int>> results = [];
    results.add(values);
    while (!values.every((element) => element == 0)) {
      List<int> result = [];
      for (var i = 0; i < values.length - 1; i++) {
        result.add(values[i + 1] - values[i]);
      }
      values = result;
      results.add(result);
    }
    for (var i = results.length - 2; i >= 0; i--) {
      var result = results[i];
      result.add(result.last + results[i + 1].last);
      results[i] = result;
    }
    total += results[0].last;
    // print(results[0].last);
  }
  print(total);
}

void part2(var report) {
  int total = 0;
  for (var values in report) {
    List<List<int>> results = [];
    results.add(values);
    while (!values.every((element) => element == 0)) {
      List<int> result = [];
      for (var i = 0; i < values.length - 1; i++) {
        result.add(values[i + 1] - values[i]);
      }
      values = result;
      results.add(result);
    }
    for (var i = results.length - 2; i >= 0; i--) {
      var result = results[i];
      result.insert(0, result.first - results[i + 1].first);
      results[i] = result;
    }
    total += results[0].first;
    // print(results[0].first);
  }
  print(total);
}

void main() {
  List<List<int>> report = [];
  var line;
  while ((line = stdin.readLineSync()) != null) {
    report.add(line!.split(' ').map((e) => int.parse(e)).cast<int>().toList());
  }

  part1(report);
  part2(report);
}
