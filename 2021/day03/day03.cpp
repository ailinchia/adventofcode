#include <string>
#include <iostream>
#include <vector>
#include <list>

void part1(const std::vector<std::string> &input) {
    auto numLen = input[0].length();

    uint gamma = 0;
    uint epsilon = 0;
    for (auto i = 0; i < numLen; ++i) {
        uint countOne = 0;
        for (auto num : input) {
            if (num[i] == '1') {
                ++countOne;
            }
        }

        gamma <<= 1;
        epsilon <<= 1;
        if (countOne > (input.size() / 2)) {
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
    auto ogrInput = std::list<std::string>(input.begin(), input.end());
    for (auto i = 0; i < numLen; ++i) {
        uint countZero = 0;
        uint countOne = 0;
        for (auto num : ogrInput) {
            if (num[i] == '0') {
                ++countZero;
            } else {
                ++countOne;
            }
        }

        auto keepBit = '0';
        if (countOne >= countZero) {
            keepBit = '1';
        }

        if (ogrInput.size() > 1) {
            auto it = ogrInput.begin();
            while (it != ogrInput.end()) {
                if (it->c_str()[i] == keepBit) {
                    ++it;
                } else {
                    it = ogrInput.erase(it);
                }
            }
        }

        if (ogrInput.size() == 1) {
            break;
        }
    }

    // CO2 scrubber rating
    auto csrInput = std::list<std::string>(input.begin(), input.end());
    for (auto i = 0; i < numLen; ++i) {
        uint countZero = 0;
        uint countOne = 0;
        for (auto num : csrInput) {
            if (num[i] == '0') {
                ++countZero;
            } else {
                ++countOne;
            }
        }

        auto keepBit = '1';
        if (countZero <= countOne) {
            keepBit = '0';
        }

        auto it = csrInput.begin();
        while (it != csrInput.end()) {
            if (it->c_str()[i] == keepBit) {
                ++it;
            } else {
                it = csrInput.erase(it);
            }
        }

        if (csrInput.size() == 1) {
            break;
        }
    }

    auto ogr = std::stoi(ogrInput.begin()->c_str(), nullptr, 2);
    auto csr = std::stoi(csrInput.begin()->c_str(), nullptr, 2);
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