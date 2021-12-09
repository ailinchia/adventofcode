#include <string>
#include <iostream>
#include <vector>
#include <algorithm>

void part1(const std::vector<std::string> &input) {
    int sum = 0;
    for (int i = 0; i < input.size(); i++) {
        for (int j = 0; j < input[i].length(); j++) {
            bool lowest = true;

            if (i - 1 >= 0) {
                if (input[i - 1][j] <= input[i][j]) {
                    lowest = false;
                }
            }

            if (j - 1 >= 0) {
                if (input[i][j - 1] <= input[i][j]) {
                    lowest = false;
                }
            }

            if (j + 1 < input[i].length()) {
                if (input[i][j + 1] <= input[i][j]) {
                    lowest = false;
                }
            }

            if (i + 1 < input.size()) {
                if (input[i + 1][j] <= input[i][j]) {
                    lowest = false;
                }
            }

            if (lowest) {
                sum += (input[i][j] - '0' + 1);
            }
        }
    }
    std::cout << sum << std::endl;
}

void printMap(const std::vector<std::string> &heightMap) {
    for (int i = 0; i < heightMap.size(); i++) {
        std::cout << heightMap[i] << std::endl;
    }
}

void setNeighbour(std::vector<std::string> &heightMap, int i, int j) {
    if (i - 1 >= 0) {
        auto h = heightMap[i - 1][j];
        if (h >= '0' && h <= '8') {
            heightMap[i - 1][j] = 'o';
            setNeighbour(heightMap, i - 1, j);
        }
    }

    if (j - 1 >= 0) {
        auto h = heightMap[i][j - 1];
        if (h >= '0' && h <= '8') {
            heightMap[i][j - 1] = 'o';
            setNeighbour(heightMap, i, j - 1);
        }
    }

    if (j + 1 < heightMap[i].length()) {
        auto h = heightMap[i][j + 1];
        if (h >= '0' && h <= '8') {
            heightMap[i][j + 1] = 'o';
            setNeighbour(heightMap, i, j + 1);
        }
    }

    if (i + 1 < heightMap.size()) {
        auto h = heightMap[i + 1][j];
        if (h >= '0' && h <= '8') {
            heightMap[i + 1][j] = 'o';
            setNeighbour(heightMap, i + 1, j);
        }
    }
}

int countBasinSize(std::vector<std::string> &heightMap) {
    int sum = 0;
    for (int i = 0; i < heightMap.size(); i++) {
        sum += std::count(heightMap[i].begin(), heightMap[i].end(), 'o');
        std::replace(heightMap[i].begin(), heightMap[i].end(), 'o', 'x');
    }
    return sum;
}

void part2(const std::vector<std::string> &input) {
    std::vector<std::string> heightMap = input;
    std::vector<int> basins;
    for (int i = 0; i < heightMap.size(); i++) {
        for (int j = 0; j < heightMap[i].length(); j++) {
            auto h = heightMap[i][j];
            if (h >= '0' && h <= '8') {
                heightMap[i][j] = 'o';
                setNeighbour(heightMap, i, j);
                basins.push_back(countBasinSize(heightMap));
            }
        }
    }
    std::sort(basins.rbegin(), basins.rend());
    std::cout << basins[0] * basins[1] * basins[2] << std::endl;
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