#include <string>
#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>

typedef std::vector<std::vector<int>> bingoBoard;

std::vector<std::string> split(const std::string &str, char delimiter) {
    std::vector<std::string> elements;
    std::stringstream ss(str);
    std::string element;
    while (std::getline(ss, element, delimiter)) {
        elements.push_back(element);
    }
    return elements;
}

void printBoard(const bingoBoard &board) {
    auto size = board.size();
    for (auto y = 0; y < size; ++y) {
        for (auto x = 0; x < size; ++x) {
            if (board[y][x] == -1) {
                std::cout << "x";
            } else {
                std::cout << board[y][x];
            }
            std::cout << '\t';
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

bool checkBingo(uint draw, bingoBoard &board) {
    auto size = board.size();
    bool found = false;
    for (auto y = 0; y < size && !found; ++y) {
        for (auto x = 0; x < size && !found; ++x) {
            if (board[y][x] == draw) {
                board[y][x] = -1;
                found = true;
            }
        }
    }

    // check rows
    for (auto y = 0; y < size; ++y) {
        int count = 0;
        for (auto x = 0; x < size; ++x) {
            if (board[y][x] == -1) {
                ++count;
            }
        }
        if (count == size) {
            return true;
        }
    }

    // check columns
    for (auto x = 0; x < size; ++x) {
        int count = 0;
        for (auto y = 0; y < size; ++y) {
            if (board[y][x] == -1) {
                ++count;
            }
        }
        if (count == size) {
            return true;
        }
    }
    return false;
}

int countScore(uint draw, bingoBoard &board) {
    int sum = 0;
    for (auto y = 0; y < board.size(); ++y) {
        for (auto x = 0; x < board.size(); ++x) {
            if (board[y][x] != -1) {
                sum += board[y][x];
            }
        }
    }
    return sum * draw;
}

void part1(const std::vector<uint> &draws, std::vector<bingoBoard> boards) {
    for (auto draw: draws) {
        for (auto &board : boards) {
            if (checkBingo(draw, board)) {
                std::cout << countScore(draw, board) << std::endl;
                return;
            }
        }
    }
}

void part2(const std::vector<uint> &draws, std::vector<bingoBoard> boards) {
    for (auto draw: draws) {
        for (auto it = boards.begin(); it != boards.end(); ){
            if (checkBingo(draw, *it)) {
                if (boards.size() == 1) {
                    std::cout << countScore(draw, *boards.begin()) << std::endl;
                    return;
                }
                it = boards.erase(it);
            } else {
                it++;
            }
        }
    }
}

int main() {
    std::string line;

    // get number draws
    if (!std::getline(std::cin, line)) {
        exit(1);
    }
    std::vector<uint> draws;
    auto drawStrs = split(line, ',');
    std::transform(drawStrs.begin(), drawStrs.end(), std::back_inserter(draws), [](std::string s) -> uint { return std::stoi(s, nullptr, 10 );});

    // get boards
    std::vector<bingoBoard> boards;
    bingoBoard board;
    while (std::getline(std::cin, line)) {
        if (line.length() == 0) {
            // new board
            if (!board.empty()) {
                boards.push_back(board);;
                board.clear();
            }

            continue;
        }

        int a, b, c, d, e = 0;
        std::istringstream in(line);
        in >> a >> b >> c >> d >> e;

        std::vector<int> row = {a, b, c, d, e};
        board.push_back(row);
    }
    if (!board.empty()) {
        boards.push_back(board);
    }

    part1(draws, boards);
    part2(draws, boards);

    return 0;
}