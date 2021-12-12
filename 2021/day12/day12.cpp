#include <string>
#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>
#include <unordered_map>
#include <list>
#include <cctype>

std::vector<std::string> split(const std::string &str, char delimiter) {
    std::vector<std::string> elements;
    std::stringstream ss(str);
    std::string element;
    while (std::getline(ss, element, delimiter)) {
        elements.push_back(element);
    }
    return elements;
}

int countSubstring(const std::string &str, const std::string &sub) {
    if (sub.length() == 0) {
        return 0;
    }

    int count = 0;
    for (auto offset = str.find(sub); offset != std::string::npos; offset = str.find(sub, offset + sub.length())) {
        ++count;
    }
    return count;
}

void walkGraph1(const std::unordered_map<std::string, std::list<std::string>> &graph, const std::string currentEdge, std::string currentPath, int &totalPath) {
    currentPath += currentEdge + ',';

    auto edges = graph.find(currentEdge);
    if (edges != graph.end()) {
        for (auto edge : edges->second) {
            if (edge == "start") {
                continue;
            }

            if (edge == "end") {
                totalPath++;
                continue;
            }

            bool isSmallCave = std::all_of(edge.cbegin(), edge.cend(), ::islower);
            if (isSmallCave) {
                // no repeats
                if (countSubstring(currentPath, edge) > 0) {
                    continue;
                }
            }

            walkGraph1(graph, edge, currentPath, totalPath);
        }
    }
}

void part1(const std::vector<std::pair<std::string, std::string>> &input) {
    std::unordered_map<std::string, std::list<std::string>> graph;
    for (auto in : input) {
        graph[in.first].push_back(in.second);
        graph[in.second].push_back(in.first);
    }
    int totalPath = 0;
    walkGraph1(graph, "start", "", totalPath);
    std::cout << totalPath << std::endl;
}

void walkGraph2(const std::unordered_map<std::string, std::list<std::string>> &graph, const std::string currentEdge, std::string currentPath, int &totalPath, bool hasRepeat) {
    currentPath += currentEdge + ',';

    auto edges = graph.find(currentEdge);
    if (edges != graph.end()) {
        for (auto edge : edges->second) {
            bool currentHasRepeat = hasRepeat;

            if (edge == "start") {
                continue;
            }

            if (edge == "end") {
                totalPath++;
                continue;
            }

            bool isSmallCave = std::all_of(edge.cbegin(), edge.cend(), ::islower);
            if (isSmallCave) {
                // only repeat once
                int max_count = hasRepeat ? 0 : 1;
                int count = countSubstring(currentPath, edge);
                if (count > max_count) {
                    continue;
                }

                if (count == 1) {
                    currentHasRepeat = true;
                }
            }

            walkGraph2(graph, edge, currentPath, totalPath, currentHasRepeat);
        }
    }
}

void part2(const std::vector<std::pair<std::string, std::string>> &input) {
    std::unordered_map<std::string, std::list<std::string>> graph;
    for (auto in : input) {
        graph[in.first].push_back(in.second);
        graph[in.second].push_back(in.first);
    }
    int totalPath = 0;
    walkGraph2(graph, "start", "", totalPath, false);
    std::cout << totalPath << std::endl;
}

int main() {
    std::string line;
    std::vector<std::pair<std::string, std::string>> input;

    while (std::getline(std::cin, line)) {
        if (line.empty()) {
            break;
        }

        auto tokens = split(line, '-');
        input.push_back(std::make_pair(tokens[0], tokens[1]));
    }

    part1(input);
    part2(input);

    return 0;
}