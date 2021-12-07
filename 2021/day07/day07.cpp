#include <string>
#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>

std::vector<std::string> split(const std::string &str, char delimiter) {
    std::vector<std::string> elements;
    std::stringstream ss(str);
    std::string element;
    while (std::getline(ss, element, delimiter)) {
        elements.push_back(element);
    }
    return elements;
}

void part1(const std::vector<uint> &inputs) {
    uint minTotalFuel = UINT32_MAX;
    auto min = std::min_element(inputs.begin(), inputs.end());
    auto max = std::max_element(inputs.begin(), inputs.end());

    for (auto i = *min; i <= *max; i++) {
        int totalFuel = 0;
        for ( auto input : inputs) {
            totalFuel += (std::max(input, i) - std::min(input, i));
        }
        if (totalFuel < minTotalFuel) {
            minTotalFuel = totalFuel;
        }
    }

    std::cout << minTotalFuel << std::endl;
}

void part2(const std::vector<uint> &inputs) {
    uint minTotalFuel = UINT32_MAX;
    auto min = std::min_element(inputs.begin(), inputs.end());
    auto max = std::max_element(inputs.begin(), inputs.end());

    for (auto i = *min; i <= *max; i++) {
        int totalFuel = 0;
        for ( auto input : inputs) {
            auto steps = std::max(input, i) - std::min(input, i);
            for (auto j = 1; j <= steps; j++) {
                totalFuel += j;
            }
        }
        if (totalFuel < minTotalFuel) {
            minTotalFuel = totalFuel;
        }
    }

    std::cout << minTotalFuel << std::endl;

}

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) {
        exit(1);
    }
    std::vector<uint> inputs;
    auto inputStrs = split(line, ',');
    std::transform(inputStrs.begin(), inputStrs.end(), std::back_inserter(inputs), [](std::string s) -> uint { return std::stoi(s);});
    std::sort(inputs.begin(), inputs.end());
    part1(inputs);
    part2(inputs);

    return 0;
}