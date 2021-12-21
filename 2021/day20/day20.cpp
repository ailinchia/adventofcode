#include <string>
#include <iostream>
#include <map>
#include <algorithm>

void printImage(const std::map<int, std::map<int, int>> &input) {
    auto image = input;

    auto minX = image.begin()->first;
    auto maxX = image.rbegin()->first;
    auto minY = image.begin()->second.begin()->first;
    auto maxY = image.begin()->second.rbegin()->first;

    for (int y = minY; y <= maxY; y++) {
        for (int x = minX; x <= maxX; x++) {
            std::cout << (char)(image[x][y] ? '#' : '.');
        }
        std::cout << std::endl;
    }
}

unsigned countLit(const std::map<int, std::map<int, int>> &image) {
    unsigned count = 0;
    for (auto it = image.begin(); it != image.end(); it++) {
        for (auto it2 = it->second.begin(); it2 != it->second.end(); it2++) {
            count += it2->second;
        }
    }
    return count;
}

std::string getBinaryOutput(const std::map<int, std::map<int, int>> &image, int step, int x, int y) {
    auto itx = image.find(x);
    if (itx != image.end()) {
        auto ity = itx->second.find(y);
        if (ity != itx->second.end()) {
            return std::to_string(ity->second);
        }
    }

    return (step % 2 == 0) ? std::string("0") : std::string("1");
}

int main() {
    // get image enhancement algorithm
    std::string iea;
    if (!std::getline(std::cin, iea)) {
        exit(1);
    }

    // get input image
    std::string line;
    std::map<int, std::map<int, int>> image;

    int y = 0;
    while (std::getline(std::cin, line)) {
        if (line.length() == 0) {
            continue;
        }
        for (unsigned x = 0; x < line.size(); x++) {
            image[x][y] = (line[x] == '#') ? 1 : 0;
        }
        y += 1;
    }

    std::map<int, std::map<int, int>> output;

    for (int step = 0; step < 50; step++) {
        auto minX = image.begin()->first;
        auto maxX = image.rbegin()->first;
        auto minY = image.begin()->second.begin()->first;
        auto maxY = image.begin()->second.rbegin()->first;

        for (int y = minY - 2; y <= maxY + 1; y++) {
            for (int x = minX - 2; x <= maxX + 1; x++) {
                std::string binaryOutput;

                // y - 1, x - 1
                binaryOutput += getBinaryOutput(image, step, x - 1, y - 1);
                // y - 1, x
                binaryOutput += getBinaryOutput(image, step, x, y - 1);
                // y - 1, x + 1
                binaryOutput += getBinaryOutput(image, step, x + 1, y - 1);
                // y, x - 1
                binaryOutput += getBinaryOutput(image, step, x - 1, y);
                // y, x
                binaryOutput += getBinaryOutput(image, step, x, y);
                // y, x + 1
                binaryOutput += getBinaryOutput(image, step, x + 1, y);
                // y + 1, x - 1
                binaryOutput += getBinaryOutput(image, step, x - 1, y + 1);
                // y + 1, x
                binaryOutput += getBinaryOutput(image, step, x, y + 1);
                // y + 1, x + 1
                binaryOutput += getBinaryOutput(image, step, x + 1, y + 1);

                auto pos = std::stoi(binaryOutput, nullptr, 2);

                output[x][y] = (iea[pos] == '#') ? 1 : 0;
            }
        }

        image = output;
        if (step == 1) {
            // part 1
            std::cout << countLit(image) << std::endl;
        }
    }

    // part 2
    std::cout << countLit(image) << std::endl;

    return 0;
}