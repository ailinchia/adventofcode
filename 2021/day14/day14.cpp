#include <string>
#include <iostream>
#include <vector>
#include <sstream>
#include <unordered_map>

std::vector<std::string> split(const std::string &str, char delimiter) {
    std::vector<std::string> elements;
    std::stringstream ss(str);
    std::string element;
    while (std::getline(ss, element, delimiter)) {
        elements.push_back(element);
    }
    return elements;
}

void part1(const std::string &polymerTemplate, const std::unordered_map<std::string, std::string> &rules) {
    std::unordered_map<std::string, std::string> rulesMap = rules;
    std::unordered_map<std::string, uint64_t> polymerCount;
    std::unordered_map<char, uint64_t> elementCount;

    for (unsigned i = 0; i + 1 < polymerTemplate.size(); i++) {
        std::string polymerPair = std::string(polymerTemplate.c_str() + i, 2);
        polymerCount[polymerPair] += 1;
        elementCount[polymerPair.front()] += 1;
    }
    elementCount[polymerTemplate.back()] += 1;

    for (int i = 0; i < 10; i++) {
        auto newPolymerCount = polymerCount;
        for (auto kv = polymerCount.begin(); kv != polymerCount.end(); kv++) {
            std::string firstPolymer, secondPolymer;
            auto insertElement = rulesMap[kv->first];
            firstPolymer.append(1, kv->first.front());
            firstPolymer.append(insertElement);
            secondPolymer.append(insertElement);
            secondPolymer.append(1, kv->first.back());

            newPolymerCount[firstPolymer] += kv->second;
            newPolymerCount[secondPolymer] += kv->second;
            newPolymerCount[kv->first] -= kv->second;
            elementCount[insertElement.front()] += kv->second;
        }
        polymerCount = newPolymerCount;
    }

    uint64_t minCount = UINT64_MAX;
    uint64_t maxCount = 0;
    for (auto kv = elementCount.begin(); kv != elementCount.end(); kv++) {
        maxCount = std::max(maxCount, kv->second);
        minCount = std::min(minCount, kv->second);
    }
    std::cout << maxCount - minCount << std::endl;
}

void part2(const std::string &polymerTemplate, const std::unordered_map<std::string, std::string> &rules) {
    std::unordered_map<std::string, std::string> rulesMap = rules;
    std::unordered_map<std::string, uint64_t> polymerCount;
    std::unordered_map<char, uint64_t> elementCount;

    for (unsigned i = 0; i + 1 < polymerTemplate.size(); i++) {
        std::string polymerPair = std::string(polymerTemplate.c_str() + i, 2);
        polymerCount[polymerPair] += 1;
        elementCount[polymerPair.front()] += 1;
    }
    elementCount[polymerTemplate.back()] += 1;

    for (int i = 0; i < 40; i++) {
        auto newPolymerCount = polymerCount;
        for (auto kv = polymerCount.begin(); kv != polymerCount.end(); kv++) {
            std::string firstPolymer, secondPolymer;
            auto insertElement = rulesMap[kv->first];
            firstPolymer.append(1, kv->first.front());
            firstPolymer.append(insertElement);
            secondPolymer.append(insertElement);
            secondPolymer.append(1, kv->first.back());

            newPolymerCount[firstPolymer] += kv->second;
            newPolymerCount[secondPolymer] += kv->second;
            newPolymerCount[kv->first] -= kv->second;
            elementCount[insertElement.front()] += kv->second;
        }
        polymerCount = newPolymerCount;
    }

    uint64_t minCount = UINT64_MAX;
    uint64_t maxCount = 0;
    for (auto kv = elementCount.begin(); kv != elementCount.end(); kv++) {
        maxCount = std::max(maxCount, kv->second);
        minCount = std::min(minCount, kv->second);
    }
    std::cout << maxCount - minCount << std::endl;
}

int main() {
    std::string polymerTemplate;
    if (!std::getline(std::cin, polymerTemplate)) {
        exit(1);
    }

    std::string pairElements, token, insertionElement;
    std::unordered_map<std::string, std::string> rules;
    while (std::cin >> pairElements >> token >> insertionElement) {
        rules[pairElements] = insertionElement;
    }

    part1(polymerTemplate, rules);
    part2(polymerTemplate, rules);

    return 0;
}