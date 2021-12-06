#include <string>
#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>
#include <map>
#include <numeric>

std::vector<std::string> split(const std::string &str, char delimiter) {
    std::vector<std::string> elements;
    std::stringstream ss(str);
    std::string element;
    while (std::getline(ss, element, delimiter)) {
        elements.push_back(element);
    }
    return elements;
}

uint64_t countFish(std::map<uint, uint64_t> inputMap, uint numDays) {
    for (uint day = 0; day < numDays; day++) {
        std::map<uint, uint64_t> newInputMap;
        for (auto im : inputMap) {
            auto count = inputMap[im.first];
            if (count == 0) {
                continue;
            }

            if (im.first == 0) {
                newInputMap[6] += count;
                newInputMap[8] += count;
            } else {
                newInputMap[im.first - 1] += count;
            }
        }
        inputMap = newInputMap;
    }

    return std::accumulate(inputMap.begin(), inputMap.end(), 0ULL, [](uint64_t value, const std::map<uint, uint64_t>::value_type &p) { return value + p.second; });
}

void part1(std::map<uint, uint64_t> inputMap, uint numDays) {
    std::cout << countFish(inputMap, numDays) << std::endl;
}

void part2(std::map<uint, uint64_t> inputMap, uint numDays) {
    std::cout << countFish(inputMap, numDays) << std::endl;
}

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) {
        exit(1);
    }
    std::vector<uint> inputs;
    auto inputStrs = split(line, ',');
    std::transform(inputStrs.begin(), inputStrs.end(), std::back_inserter(inputs), [](std::string s) -> uint { return std::stoi(s);});

    std::map<uint, uint64_t> inputMap;
    for (auto input : inputs) {
        inputMap[input] += 1;
    }

    part1(inputMap, 80);
    part2(inputMap, 256);

    return 0;
}