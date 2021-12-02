#include <string>
#include <iostream>
#include <vector>

void part1(const std::vector<uint> &input) {
    uint prev = 0;
    uint count = 0;
    for (auto current : input) {
        if (prev != 0  && current > prev) {
            ++count;
        }
        prev = current;
    }
    std::cout << count << std::endl;
}

void part2(const std::vector<uint> &input) {
    uint prev = 0;
    uint current = 0;
    uint count = 0;
    for (int i = 0; i < input.size(); ++i) {
        if (i + 2 >= input.size()) {
            break;
        }
        current = input[i] + input[i + 1] + input[i + 2];
        if (prev != 0  && current > prev) {
            ++count;
        }
        prev = current;
    }
    std::cout << count << std::endl;
}

int main() {
    std::string line;
    std::vector<uint> input;

    while (std::getline(std::cin, line)) {
        input.push_back(std::stoi(line));
    }

    part1(input);
    part2(input);

    return 0;
}