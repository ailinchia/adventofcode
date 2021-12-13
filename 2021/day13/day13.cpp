#include <string>
#include <iostream>
#include <vector>
#include <sstream>

static const int MAX_GRID_SIZE = 1500;

std::vector<std::string> split(const std::string &str, char delimiter) {
    std::vector<std::string> elements;
    std::stringstream ss(str);
    std::string element;
    while (std::getline(ss, element, delimiter)) {
        elements.push_back(element);
    }
    return elements;
}

void printGrid(const char grid[MAX_GRID_SIZE][MAX_GRID_SIZE], int maxX, int maxY) {
    for (int y = 0; y <= maxY; y++) {
        for (int x = 0; x <= maxX; x++) {
            std::cout << (grid[x][y] ?: ' ');
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

uint countGrid(const char grid[MAX_GRID_SIZE][MAX_GRID_SIZE], int maxX, int maxY) {
    uint count = 0;
    for (auto y = 0; y <= maxY; y++) {
        for (auto x = 0; x <= maxX; x++) {
            if (grid[x][y] == '#') {
                count++;
            }
        }
    }
    return count;
}

void part1(const std::vector<std::pair<int, int>> &coordinates, const std::vector<std::pair<char, int>> &folds) {
    char grid[MAX_GRID_SIZE][MAX_GRID_SIZE] = {};
    int maxX, maxY = 0;
    for (auto coord : coordinates) {
        maxX = std::max(maxX, coord.first);
        maxY = std::max(maxY, coord.second);
        grid[coord.first][coord.second] = '#';
    }

    for (auto fold : folds) {
        if (fold.first == 'x') {
            maxX = fold.second;
            for (int x = fold.second + 1; x < fold.second * 2 + 1; x++) {
                for (int y = 0; y <= maxY; y++) {
                    grid[(fold.second * 2) - x][y] |= grid[x][y];
                    grid[x][y] = '\0';
                }
            }
        } else {
            maxY = fold.second;
            for (int x = 0; x <= maxX; x++) {
                for (int y = fold.second + 1; y < fold.second * 2 + 1; y++) {
                    grid[x][(fold.second * 2) - y] |= grid[x][y];
                    grid[x][y] = '\0';
                }
            }
        }
        break;
    }
    std::cout << countGrid(grid, maxX, maxY) << std::endl;
}

void part2(const std::vector<std::pair<int, int>> &coordinates, const std::vector<std::pair<char, int>> &folds) {
    char grid[MAX_GRID_SIZE][MAX_GRID_SIZE] = {};
    int maxX, maxY = 0;
    for (auto coord : coordinates) {
        maxX = std::max(maxX, coord.first);
        maxY = std::max(maxY, coord.second);
        grid[coord.first][coord.second] = '#';
    }

    for (auto fold : folds) {
        if (fold.first == 'x') {
            maxX = fold.second;
            for (int x = fold.second + 1; x < fold.second * 2 + 1; x++) {
                for (int y = 0; y <= maxY; y++) {
                    grid[(fold.second * 2) - x][y] |= grid[x][y];
                    grid[x][y] = '\0';
                }
            }
        } else {
            maxY = fold.second;
            for (int x = 0; x <= maxX; x++) {
                for (int y = fold.second + 1; y < fold.second * 2 + 1; y++) {
                    grid[x][(fold.second * 2) - y] |= grid[x][y];
                    grid[x][y] = '\0';
                }
            }
        }
    }
    printGrid(grid, maxX, maxY);
}

int main() {
    static const std::string foldAlongStr = "fold along";

    std::string line;
    std::vector<std::pair<int, int>> coordinates;
    std::vector<std::pair<char, int>> folds;

    while (std::getline(std::cin, line)) {
        if (line.empty()) {
            continue;
        }

        if (std::equal(foldAlongStr.begin(), foldAlongStr.end(), line.begin())) {
            auto tokens = split(line, ' ');
            folds.push_back(std::make_pair(tokens[2][0], stoi(tokens[2].substr(2))));
        } else {
            auto tokens = split(line, ',');
            coordinates.push_back(std::make_pair(std::stoi(tokens[0]), std::stoi(tokens[1])));
        }
    }

    part1(coordinates, folds);
    part2(coordinates, folds);

    return 0;
}