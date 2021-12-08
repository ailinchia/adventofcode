#include <string>
#include <iostream>
#include <vector>
#include <sstream>
#include <map>
#include <algorithm>
#include <cassert>

std::vector<std::string> split(const std::string &str, char delimiter) {
    std::vector<std::string> elements;
    std::stringstream ss(str);
    std::string element;
    while (std::getline(ss, element, delimiter)) {
        if (element.empty()) {
            continue;
        }
        elements.push_back(element);
    }
    return elements;
}

// 1 - 2
// 4 - 4
// 7 - 3
// 8 - 7
void part1(const std::vector<std::pair<std::vector<std::string>, std::vector<std::string>>> &inputs) {
    int count = 0;
    for (auto input : inputs) {
        for (auto item : input.second) {
            if (item.length() >= 1 && item.length() <= 4 || item.length() == 7) {
                count++;
            }
        }
    }
    std::cout << count << std::endl;
}

bool find(std::string str, std::string sub) {
    auto sum = 0;
    for (auto c : sub) {
        if (str.find(c) != std::string::npos) {
            sum++;
        }
    }
    return (sum == sub.length());
}

void part2(const std::vector<std::pair<std::vector<std::string>, std::vector<std::string>>> &inputs) {
    int count = 0;

    for (auto input : inputs) {
        std::map<int, std::string> inputMaps;
        std::string a,b,c,d,e,f,g;
        while (true) {
            for (auto item : input.first) {
                std::sort(item.begin(), item.end());
                switch (item.length()) {
                    case 2:
                        inputMaps[1] = item;
                        break;
                    case 3:
                        inputMaps[7] = item;
                        break;
                    case 4:
                        inputMaps[4] = item;
                        break;
                    case 5: {
                        // 3 (1 / 7 is subset)
                        auto it1 = inputMaps.find(1);
                        auto it7 = inputMaps.find(7);
                        if ((it1 != inputMaps.end() && find(item, it1->second)) ||
                            (it7 != inputMaps.end() && find(item, it7->second))) {
                            inputMaps[3] = item;
                        }

                        auto it3 = inputMaps.find(3);
                        if (!e.empty() && it3->second != item) {
                            if (item.find(e[0]) != std::string::npos) {
                                inputMaps[2] = item;
                            } else {
                                inputMaps[5] = item;
                            }
                        }
                    } break;
                    case 6: {
                        // 0
                        // 6 (5 + e)
                        // 9 (4 is subset)
                        auto it4 = inputMaps.find(4);
                        if (it4 != inputMaps.end()) {
                            if (find(item, it4->second)) {
                                inputMaps[9] = item;
                            }
                        }
                    } break;
                    case 7:
                        inputMaps[8] = item;
                        break;
                }
            }

            auto it5 = inputMaps.find(5);
            if (!e.empty() && it5 != inputMaps.end()) {
                auto s = it5->second;
                s += e;
                std::sort(s.begin(), s.end());
                inputMaps[6] = s;
            }

            auto it1 = inputMaps.find(1);
            auto it7 = inputMaps.find(7);
            if (a.empty() && it1 != inputMaps.end() && it7 != inputMaps.end()) {
                std::set_difference(it7->second.begin(), it7->second.end(), it1->second.begin(), it1->second.end(), std::back_inserter(a));
                assert(a.length() == 1);
            }

            auto it9 = inputMaps.find(9);
            if (it9 != inputMaps.end()) {
                auto it3 = inputMaps.find(3);
                if (b.empty() && it3 != inputMaps.end()) {
                    std::set_difference(it9->second.begin(), it9->second.end(), it3->second.begin(), it3->second.end(), std::back_inserter(b));
                    assert(b.length() == 1);
                }
            }

            auto it8 = inputMaps.find(8);
            if (it8 != inputMaps.end()) {
                auto it6 = inputMaps.find(6);
                if (c.empty() && it6 != inputMaps.end()) {
                    std::set_difference(it8->second.begin(), it8->second.end(), it6->second.begin(), it6->second.end(), std::back_inserter(c));
                    assert(c.length() == 1);
                }

                auto it9 = inputMaps.find(9);
                if (e.empty() && it9 != inputMaps.end()) {
                    std::set_difference(it8->second.begin(), it8->second.end(), it9->second.begin(), it9->second.end(), std::back_inserter(e));
                    assert(e.length() == 1);
                }
            }

            if (f.empty() && !e.empty()) {
                auto it2 = inputMaps.find(2);
                auto it3 = inputMaps.find(3);
                if (it2 != inputMaps.end() && it3 != inputMaps.end()) {
                    std::string ef;
                    std::set_symmetric_difference(it2->second.begin(), it2->second.end(), it3->second.begin(), it3->second.end(), std::back_inserter(ef));
                    f = ef;
                    f.erase(f.find(e), 1);
                    assert(f.length() == 1);
                }
            }

            if (g.empty() && !a.empty() && !b.empty()) {
                auto it3 = inputMaps.find(3);
                auto it4 = inputMaps.find(4);
                if (it3 != inputMaps.end() && it4 != inputMaps.end()) {
                    std::string abg;
                    std::set_symmetric_difference(it3->second.begin(), it3->second.end(), it4->second.begin(), it4->second.end(), std::back_inserter(abg));
                    g = abg;
                    g.erase(g.find(a), 1);
                    g.erase(g.find(b), 1);
                    assert(g.length() == 1);
                }
            }

            if (d.empty() && it8 != inputMaps.end() && !a.empty() && !b.empty() && !c.empty() && !e.empty() && !f.empty() && !g.empty()) {
                std::string abcefg = a + b + c + e + f + g;
                std::sort(abcefg.begin(), abcefg.end());
                inputMaps[0] = abcefg;

                std::set_difference(it8->second.begin(), it8->second.end(), abcefg.begin(), abcefg.end(), std::back_inserter(d));
            }

            if (inputMaps.size() == 10) {
                break;
            }
        }

        std::map<std::string, int> outputMaps;
        for (auto kv : inputMaps) {
            outputMaps[kv.second] = kv.first;
        }

        std::string output;
        for (auto item : input.second) {
            std::sort(item.begin(), item.end());
            output += std::to_string(outputMaps[item]);
        }
        count += std::stoi(output);
    }
    std::cout << count << std::endl;
}

int main() {
    std::string line;
    std::vector<std::pair<std::vector<std::string>, std::vector<std::string>>> inputs;
    while (std::getline(std::cin, line)) {
        if (line.empty()) {
            continue;
        }

        auto inputStrs = split(line, '|');
        auto signalPatterns = split(inputStrs[0], ' ');
        auto outputValues = split(inputStrs[1], ' ');
        inputs.push_back(std::make_pair(signalPatterns, outputValues));
    }

    part1(inputs);
    part2(inputs);

    return 0;
}