#include <string>
#include <iostream>
#include <vector>
#include <algorithm>

void printCave(const std::vector<std::string> &cave) {
    for (int i = 0; i < cave.size(); i++) {
        std::cout << cave[i] << std::endl;
    }
    std::cout << std::endl;
}

bool increaseEnergy(std::vector<std::string> &cave, int i, int j) {
    if (cave[i][j] != '0') {
        cave[i][j] += 1;
    }
    return (cave[i][j] > '9');
}

bool flashOctopus(std::vector<std::string> &cave, int i, int j) {
    bool moreFlash = false;
    if (i - 1 >= 0) {
        if (j - 1 >= 0) {
            moreFlash |= increaseEnergy(cave, i - 1, j - 1);
        }

        moreFlash |= increaseEnergy(cave, i - 1, j);

        if (j + 1 < cave[i].length()) {
            moreFlash |= increaseEnergy(cave, i - 1, j + 1);
        }
    }

    if (j - 1 >= 0) {
        moreFlash |= increaseEnergy(cave, i, j - 1);
    }

    if (j + 1 < cave[i].length()) {
        moreFlash |= increaseEnergy(cave, i, j + 1);
    }

    if (i + 1 < cave.size()) {
        if (j - 1 >= 0) {
            moreFlash |= increaseEnergy(cave, i + 1, j - 1);
        }
        moreFlash |= increaseEnergy(cave, i + 1, j);

        if (j + 1 < cave[i].length()) {
            moreFlash |= increaseEnergy(cave, i + 1, j + 1);
        }
    }
    cave[i][j] = '0';
    return moreFlash;
}

int countFlash(const std::vector<std::string> &cave) {
    int count = 0;
    for (int i = 0; i < cave.size(); i++) {
        count += std::count(cave[i].begin(), cave[i].end(), '0');
    }
    return count;
}

void part1(const std::vector<std::string> &input) {
    std::vector<std::string> cave = input;
    int total = 0;
    for (int step = 0; step < 100; step++) {
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 10; j++) {
                cave[i][j] += 1;
            }
        }

        while (true) {
            bool moreFlash = false;
            for (int i = 0; i < 10; i++) {
                for (int j = 0; j < 10; j++) {
                    if (cave[i][j] > '9') {
                        moreFlash |= flashOctopus(cave, i, j);
                    }
                }
            }

            if (!moreFlash) {
                break;
            }
        }

        total += countFlash(cave);
    }
    std::cout << total << std::endl;
}

void part2(const std::vector<std::string> &input) {
    std::vector<std::string> cave = input;
    int total = 0;
    for (int step = 0; step < 1000; step++) {
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 10; j++) {
                cave[i][j] += 1;
            }
        }

        while (true) {
            bool moreFlash = false;
            for (int i = 0; i < 10; i++) {
                for (int j = 0; j < 10; j++) {
                    if (cave[i][j] > '9') {
                        moreFlash |= flashOctopus(cave, i, j);
                    }
                }
            }

            if (!moreFlash) {
                break;
            }
        }

        total += countFlash(cave);
        if (countFlash(cave) == 100) {
            std::cout << step + 1 << std::endl;
            break;
        }
    }
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