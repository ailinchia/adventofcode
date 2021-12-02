#include <string>
#include <iostream>
#include <vector>

void part1(const std::vector<std::pair<std::string, uint>> &input) {
    int pos = 0;
    int depth = 0;
    for (auto current : input) {
        if (current.first == "forward") {
            pos += current.second;
        } else if (current.first == "up") {
            depth -= current.second;
        } else if (current.first == "down") {
            depth += current.second;
        }
    }
    std::cout << pos * depth << std::endl;
}

void part2(const std::vector<std::pair<std::string, uint>> &input) {
    int pos = 0;
    int depth = 0;
    int aim = 0;
    for (auto current : input) {
        if (current.first == "forward") {
            pos += current.second;
            depth += aim * current.second;
        } else if (current.first == "up") {
            aim -= current.second;
        } else if (current.first == "down") {
            aim += current.second;
        }
    }
    std::cout << pos * depth << std::endl;
}

int main() {
    std::string direction;
    uint units = 0;
    std::vector<std::pair<std::string, uint>> input;

    while (std::cin >> direction >> units) {
        input.push_back(std::make_pair(direction, units));
    }

    part1(input);
    part2(input);

    return 0;
}