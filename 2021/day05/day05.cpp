#include <string>
#include <iostream>
#include <vector>
#include <sstream>

typedef std::pair<uint, uint> Coordinate;

static const uint MAX_GRID_SIZE = 1000;


std::vector<std::string> split(const std::string &str, char delimiter) {
    std::vector<std::string> elements;
    std::stringstream ss(str);
    std::string element;
    while (std::getline(ss, element, delimiter)) {
        elements.push_back(element);
    }
    return elements;
}

std::pair<uint, uint> makeCoordinate(std::string cStr) {
    auto tokens = split(cStr, ',');
    return std::make_pair(std::stoi(tokens[0]), std::stoi(tokens[1]));
}

void printGrid(const char grid[MAX_GRID_SIZE][MAX_GRID_SIZE]) {
    for (auto y = 0; y < MAX_GRID_SIZE; y++) {
        for (auto x = 0; x < MAX_GRID_SIZE; x++) {
            std::cout << (char)(grid[x][y] + '0') << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

uint countGrid(const char grid[MAX_GRID_SIZE][MAX_GRID_SIZE]) {
    uint count = 0;
    for (auto y = 0; y < MAX_GRID_SIZE; y++) {
        for (auto x = 0; x < MAX_GRID_SIZE; x++) {
            if (grid[x][y] >= 2) {
                count++;
            }
        }
    }
    return count;
}

void part1(const std::vector<std::pair<Coordinate, Coordinate>> &input) {
    char grid[MAX_GRID_SIZE][MAX_GRID_SIZE] = {};
    for (auto line : input) {
        auto start = line.first;
        auto end = line.second;

        // ignore diagonals
        if (start.first != end.first && start.second != end.second) {
            continue;
        }

        for (auto x = std::min(start.first, end.first); x <= std::max(start.first, end.first); x++) {
            for (auto y = std::min(start.second, end.second); y <= std::max(start.second, end.second); y++) {
                grid[y][x] += 1;
            }
        }
    }

    std::cout << countGrid(grid) << std::endl;
}

void part2(const std::vector<std::pair<Coordinate, Coordinate>> &input) {
    char grid[MAX_GRID_SIZE][MAX_GRID_SIZE] = {};
    for (auto line : input) {
        auto start = line.first;
        auto end = line.second;

        if (start.first == end.first || start.second == end.second) {
            for (auto x = std::min(start.first, end.first); x <= std::max(start.first, end.first); x++) {
                for (auto y = std::min(start.second, end.second); y <= std::max(start.second, end.second); y++) {
                    grid[y][x] += 1;
                }
            }
        } else {
            // diagonals
            uint x, y = 0;
            int xi = (start.first < end.first) ? 1 : -1;
            int yi = (start.second < end.second) ? 1 : -1;

            for (x = start.first, y = start.second; ; x += xi, y += yi) {
                grid[y][x] += 1;

                if (x == end.first || y == end.second) {
                    break;
                }
            }
        }
    }

    std::cout << countGrid(grid) << std::endl;
}

int main() {
    std::string firstStr, secondStr, separator;
    std::vector<std::pair<Coordinate, Coordinate>> input;

    while (std::cin >> firstStr >> secondStr >> secondStr) {
        input.push_back(std::make_pair(makeCoordinate(firstStr), makeCoordinate(secondStr)));
    }

    part1(input);
    part2(input);

    return 0;
}