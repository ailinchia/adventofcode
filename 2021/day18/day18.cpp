#include <string>
#include <iostream>
#include <vector>
#include <sstream>
#include <regex>
#include <cmath>

std::vector<std::string> split(const std::string &str, char delimiter) {
    std::vector<std::string> elements;
    std::stringstream ss(str);
    std::string element;
    while (std::getline(ss, element, delimiter)) {
        elements.push_back(element);
    }
    return elements;
}

uint64_t magnitudeSnailFish(std::string &currentStr) {
    static const std::regex pairRegex("\\[[0-9]{1,},[0-9]{1,}\\]");
    std::sregex_iterator it;
    do {
        for (it = std::sregex_iterator(currentStr.begin(), currentStr.end(), pairRegex); it != std::sregex_iterator(); ++it) {
            auto pair = it->str();
            pair.erase(0, 1);
            pair.erase(pair.size() - 1, 1);
            auto tokens= split(pair, ',');
            auto first = std::stol(tokens[0]);
            auto second = std::stol(tokens[1]);
            auto result = (first * 3) + (second * 2);
            currentStr.erase(it->position(), it->length());
            currentStr.insert(it->position(), std::to_string(result));
        }
        it = std::sregex_iterator(currentStr.begin(), currentStr.end(), pairRegex);
    } while (it != std::sregex_iterator());

    return std::stoull(currentStr);
}

bool explodeSnailFish(std::string &currentStr) {
    bool exploded = false;

    // find fourth '['
    size_t pos = -1;
    unsigned countOpen = 0;
    while ((pos = currentStr.find_first_of("[]", pos + 1)) != std::string::npos) {
        if (currentStr[pos] == '[') {
            countOpen++;
        } else {
            countOpen--;
        }

        if (countOpen == 5) {
            exploded = true;
            auto cPos = currentStr.find_first_of("]", pos + 1);
            auto pair = split(currentStr.substr(pos + 1, cPos - pos - 1), ',');
            auto first = std::stoi(pair[0]);
            auto second = std::stoi(pair[1]);

            currentStr.erase(pos, cPos - pos);
            currentStr[pos] = '0';

            auto rPos = currentStr.find_first_of("0123456789", pos + 1);
            if (rPos != std::string::npos) {
                auto rNpos = currentStr.find_first_not_of("0123456789", rPos);
                auto rightNumber = std::stoi(currentStr.substr(rPos, rNpos - rPos));
                currentStr.erase(rPos, rNpos - rPos);
                currentStr.insert(rPos, std::to_string(rightNumber + second));
            }

            auto lNpos = currentStr.find_last_of("0123456789", pos - 1);
            if (lNpos != std::string::npos) {
                auto lPos = currentStr.find_last_of("[,", lNpos);
                auto leftNumber = std::stoi(currentStr.substr(lPos + 1, lNpos - lPos));
                currentStr.erase(lPos + 1, lNpos - lPos);
                currentStr.insert(lPos + 1, std::to_string(leftNumber + first));
            }

            break;
        }
    }

    return exploded;
}

bool splitSnailFish(std::string &currentStr) {
    bool splited = false;
    static const std::regex digitsRegex("[0-9]{2,}");
    auto digitsBegin = std::sregex_iterator(currentStr.begin(), currentStr.end(), digitsRegex);
    if (digitsBegin != std::sregex_iterator()) {
        splited = true;
        auto digits = std::stoi(digitsBegin->str());
        std::string newPair = "[" + std::to_string(int(floor((double) digits / 2))) + "," + std::to_string(int(ceil((double) digits / 2))) + "]";
        currentStr.erase(digitsBegin->position(), digitsBegin->length());
        currentStr.insert(digitsBegin->position(), newPair);
    }

    return splited;
}

void part1(const std::vector<std::string> &input) {
    std::vector<std::string> lines = input;
    std::string currentStr;

    for (unsigned i = 0; i < input.size(); i++) {
        if (currentStr.empty()) {
            currentStr = lines[i];
        } else {
            currentStr = "[" + currentStr + "," + lines[i] + "]";
        }

        bool reduced;
        do {
            reduced = explodeSnailFish(currentStr);
            if (!reduced) {
                reduced = splitSnailFish(currentStr);
            }
        } while (reduced);
    }
    std::cout << magnitudeSnailFish(currentStr) << std::endl;
}

void part2(const std::vector<std::string> &input) {
    uint64_t maxMagnitude = 0;
    for (unsigned i = 0; i < input.size(); i++) {
        for (unsigned j = 0; j < input.size(); j++) {
            if (i == j) {
                continue;
            }
            std::string currentStr = "[" + input[i] + "," + input[j] + "]";

            bool reduced;
            do {
                reduced = explodeSnailFish(currentStr);
                if (!reduced) {
                    reduced = splitSnailFish(currentStr);
                }
            } while (reduced);

            maxMagnitude = std::max(maxMagnitude, magnitudeSnailFish(currentStr));
        }
    }
    std::cout << maxMagnitude << std::endl;
}

int main() {
    std::string line;
    std::vector<std::string> input;

    while (std::getline(std::cin, line)) {
        if (line.empty()) {
            break;
        }
        input.push_back(line);
    }

    part1(input);
    part2(input);

    return 0;
}