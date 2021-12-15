#include <queue>
#include <string>
#include <iostream>
#include <algorithm>
#include <map>

typedef std::pair<int, int> Coordinate;

std::vector<Coordinate> getNeighbours(Coordinate current, Coordinate destination) {
    std::vector<Coordinate> neighbours;

    // x - 1, y
    if (current.first > 0) {
        neighbours.push_back(std::make_pair(current.first - 1, current.second));
    }

    // x, y - 1
    if (current.second > 0) {
        neighbours.push_back(std::make_pair(current.first, current.second - 1));
    }

    // x + 1, y
    if (current.first + 1 <= destination.first) {
        neighbours.push_back(std::make_pair(current.first + 1, current.second));
    }

    // x, y + 1
    if (current.second + 1 <= destination.second) {
        neighbours.push_back(std::make_pair(current.first, current.second + 1));
    }

    return neighbours;
}

int minCost(std::map<Coordinate, int> cost, Coordinate start, Coordinate destination) {
    std::map<Coordinate, int> dp;
    std::map<Coordinate, bool> visited;

    for(int x = 0; x <= destination.first; x++) {
        for(int y = 0; y <= destination.second; y++) {
            dp[std::make_pair(x, y)] = INT32_MAX;
        }
    }

    std::priority_queue<std::pair<int, Coordinate>, std::vector<std::pair<int, Coordinate>>, std::greater<std::pair<int, Coordinate>>> pq;

    dp[start] = 0;
    pq.push({0, start});

    while (!pq.empty()) {
        auto pair = pq.top();
        pq.pop();

        auto current = pair.second;
        if (visited[current]) {
            continue;
        }

        visited[current] = true;

        for (auto neighbour : getNeighbours(current, destination)) {
            if (!visited[neighbour]) {
                dp[neighbour] = std::min(dp[neighbour], dp[current] + cost[neighbour]);
                pq.push({dp[neighbour], neighbour});
            }
        }
    }

    return dp[destination];
}

void part1(const std::vector<std::string> &input) {
    std::map<Coordinate, int> cost;
    for (unsigned y = 0; y < input.size(); y++) {
        for (unsigned x = 0; x < input[y].size(); x++) {
            cost[std::make_pair(x, y)] = input[y][x] - '0';
        }
    }

    auto start = std::make_pair(0, 0);
    auto destination = std::make_pair(input[0].size() - 1, input.size() - 1);
    std::cout << minCost(cost, start, destination) << std::endl;
}

void part2(const std::vector<std::string> &input) {
    std::map<Coordinate, int> cost;
    for (unsigned i = 0; i < 5; i++) {
        for (unsigned j = 0; j < 5; j++) {
            for (unsigned y = 0; y < input.size(); y++) {
                for (unsigned x = 0; x < input[y].size(); x++) {
                    auto c = input[y][x] - '0' + i + j;
                    if (c % 9 != 0) {
                        c %= 9;
                    }
                    cost[std::make_pair(x + (input[y].size() * j), y + (input.size() * i))] = c;
                }
            }
        }
    }

    auto start = std::make_pair(0, 0);
    auto destination = std::make_pair(input[0].size() * 5 - 1, input.size() * 5 - 1);
    std::cout << minCost(cost, start, destination) << std::endl;
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