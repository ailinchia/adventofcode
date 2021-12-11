#include <string>
#include <iostream>
#include <vector>
#include <algorithm>

bool isOpen(char c) {
    return (c == '(' || c == '[' || c == '{' || c == '<');
}

char getOpenChunk(char c) {
    switch (c) {
        case ')':
            return '(';
        case ']':
            return '[';
        case '}':
            return '{';
        case '>':
            return '<';
    }
    return '\0';
}

char getCloseChunk(char c) {
    switch (c) {
        case '(':
            return ')';
        case '[':
            return ']';
        case '{':
            return '}';
        case '<':
            return '>';
    }
    return '\0';
}

int getPart1Score(char c) {
    switch (c) {
        case ')':
            return 3;
        case ']':
            return 57;
        case '}':
            return 1197;
        case '>':
            return 25137;
    }
    return 0;
}

void part1(const std::vector<std::string> &input) {
    int score = 0;
    for (auto chunks : input) {
        std::vector<char> chunkVec;
        for (auto chunk : chunks) {
            if (isOpen(chunk)) {
                chunkVec.push_back(chunk);
            } else {
                if (chunkVec.back() == getOpenChunk(chunk)) {
                    chunkVec.pop_back();
                } else {
                    score += getPart1Score(chunk);
                    break;
                }
            }
        }
    }
    std::cout << score << std::endl;
}

int getPart2Score(char c) {
    switch (c) {
        case ')':
            return 1;
        case ']':
            return 2;
        case '}':
            return 3;
        case '>':
            return 4;
    }
    return 0;
}

void part2(const std::vector<std::string> &input) {
    std::vector<uint64_t> scores;
    for (auto chunks : input) {
        uint64_t score = 0;
        bool corrupted = false;
        std::vector<char> chunkVec;
        for (auto chunk : chunks) {
            if (isOpen(chunk)) {
                chunkVec.push_back(chunk);
            } else {
                if (chunkVec.back() == getOpenChunk(chunk)) {
                    chunkVec.pop_back();
                } else {
                    corrupted = true;
                    break;
                }
            }
        }
        if (!corrupted && !chunkVec.empty()) {
            for (auto it = chunkVec.rbegin(); it != chunkVec.rend(); it++) {
                score *= 5;
                score += getPart2Score(getCloseChunk(*it));
            }
            scores.push_back(score);
        }
    }
    std::sort(scores.begin(), scores.end());
    std::cout << scores[scores.size()/2] << std::endl;
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