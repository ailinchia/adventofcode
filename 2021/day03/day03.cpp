#include <string>
#include <iostream>
#include <vector>
#include <algorithm>

void part1(const std::vector<std::string> &input) {
    auto numLen = input[0].length();

    uint gamma = 0;
    uint epsilon = 0;
    for (auto i = 0; i < numLen; ++i) {
        uint countOne = std::count_if(input.begin(), input.end(), [i](std::string s) { return s[i] == '1'; });

        gamma <<= 1;
        epsilon <<= 1;
        if (countOne * 2 >= input.size()) {
            gamma += 1;
        } else {
            epsilon += 1;
        }
    }

    std::cout << gamma * epsilon << std::endl;
}

void part2(const std::vector<std::string> &input) {
    auto numLen = input[0].length();

    // oxygen generator rating
    auto ogrInput = std::vector<std::string>(input.begin(), input.end());
    for (auto i = 0; i < numLen && ogrInput.size() > 1; ++i) {
        uint countOne = std::count_if(ogrInput.begin(), ogrInput.end(), [i](const std::string &s) { return s[i] == '1'; });
        char keepBit = (countOne * 2 >= ogrInput.size()) ? '1' : '0';
        std::erase_if(ogrInput, [keepBit, i](const std::string &s) { return s[i] != keepBit; });
    }
    auto ogr = std::stoi(*ogrInput.begin(), nullptr, 2);

    // CO2 scrubber rating
    auto csrInput = std::vector<std::string>(input.begin(), input.end());
    for (auto i = 0; i < numLen && csrInput.size() > 1; ++i) {
        uint countZero = std::count_if(csrInput.begin(), csrInput.end(), [i](std::string s) { return s[i] == '0'; });
        char keepBit = (countZero * 2 <= csrInput.size()) ? '0' : '1';
        std::erase_if(csrInput, [keepBit, i](const std::string &s) { return s[i] != keepBit; });
    }
    auto csr = std::stoi(*csrInput.begin(), nullptr, 2);

    std::cout << ogr * csr << std::endl;
}

int main() {
    std::string line;
    std::vector<std::string> input;

    while (std::getline(std::cin, line)) {
        input.push_back(line);
    }

    part1(input);
    part2(input);

    return 0;
}