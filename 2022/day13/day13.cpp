#include <string>
#include <iostream>
#include <vector>
#include <tuple>
#include <algorithm>

//#define DEBUG_PRINT(x...)  printf(x)
#define DEBUG_PRINT(x...)

bool is_list(const std::string &s) {
    return s[0] == '[';
}

std::pair<std::string, std::string> extract_list(const std::string &input) {
    if (!is_list(input)) {
        return std::make_pair(input, "");
    }

    auto count = 0;
    for (auto i = 0; i < input.size(); i++) {
        if (input[i] == '[') {
            count += 1;
        }
        if (input[i] == ']') {
            count -= 1;
        }

        if (count == 0) {
            std::string leftover;
            if (i + 2 < input.size()) {
                leftover = input.substr(i + 2);
            }
            return std::make_pair(input.substr(1, i - 1), leftover);
        }
    }
//    printf("Error: no closing bracket found: %s\n", input.c_str());
    return std::make_pair(input, "");
}

std::string make_list(std::string s) {
    std::string n = s;
    n.insert(0, "[");
    auto i = s.find(',');
    if (i == std::string::npos) {
        n.append("]");
    } else {
        n.insert(i+1, "]");
    }
//    printf("make_list: '%s' to '%s'\n", s.c_str(), n.c_str());
    return n;
}

// return (done, result)
std::pair<bool, bool> compare_pair(std::string first, std::string second) {
    DEBUG_PRINT("compare_pair: '%s' '%s'\n", first.c_str(), second.c_str());

    if (first.empty()) {
        DEBUG_PRINT("first empty\n");
        return std::make_pair(true, true);
    }
    if (second.empty()) {
        DEBUG_PRINT("second empty\n");
        return std::make_pair(true, false);
    }

    if (first == second) {
        DEBUG_PRINT("first == second\n");
        return std::make_pair(false, false);
    }

    std::string o_first = first;
    std::string o_second = second;

    // If both values are integers, the lower integer should come first. If the left integer is lower than the right integer, the inputs are in the right order. If the left integer is higher than the right integer, the inputs are not in the right order. Otherwise, the inputs are the same integer; continue checking the next part of the input.
    if (isdigit(first[0]) && isdigit(second[0])) {
        size_t first_epos = 0;
        size_t second_epos = 0;
        auto first_int = std::stoi(first, &first_epos, 10);
        auto second_int = std::stoi(second, &second_epos, 10);
        DEBUG_PRINT("Comparing int %d and %d\n", first_int, second_int);

        if (first_int < second_int) {
            DEBUG_PRINT("Done: %s < %s\n", o_first.c_str(), o_second.c_str());
            return std::make_pair(true, true);
        } else if (first_int > second_int) {
            DEBUG_PRINT("Done: %s > %s\n", o_first.c_str(), o_second.c_str());
            return std::make_pair(true, false);
        } else {
            if (second_epos == second.size()) {
                return std::make_pair(true, false);
            }

            if (first_epos == first.size()) {
                return std::make_pair(true, true);
            }
            auto s_first = first.substr(first_epos + 1);
            auto s_second = second.substr(second_epos + 1);
            DEBUG_PRINT("Continue: %s and %s\n", s_first.c_str(), s_second.c_str());
            auto result = compare_pair(s_first, s_second);
            if (result.first) {
                return result;
            }
            DEBUG_PRINT("Error: compare_pair: %s %s\n", o_first.c_str(), o_second.c_str());
        }
    }
    // If both values are lists, compare the first value of each list, then the second value, and so on. If the left list runs out of items first, the inputs are in the right order. If the right list runs out of items first, the inputs are not in the right order. If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.
    else if (is_list(first) && is_list(second)) {
        auto f = extract_list(first);
        auto s = extract_list(second);

        if (f.first == s.first) {
            auto result = compare_pair(f.second, s.second);
            DEBUG_PRINT("list same: '%s' '%s' %s\n", f.second.c_str(), s.second.c_str(), result.second ? "true" : "false");

            if (result.first) {
                return result;
            }
            DEBUG_PRINT("Error: 1 compare_pair: %s %s\n", f.second.c_str(), s.second.c_str());
        } else {
            DEBUG_PRINT("Comparing list %s and %s\n", f.first.c_str(), s.first.c_str());
            auto result = compare_pair(f.first, s.first);
            DEBUG_PRINT("%s %s %s\n", f.first.c_str(), s.first.c_str(), result.second ? "true" : "false");

            if (result.first) {
                return result;
            }
            DEBUG_PRINT("Error: 2 compare_pair: '%s' '%s'\n", f.first.c_str(), s.first.c_str());
            result = compare_pair(f.second, s.second);
            if (result.first) {
                return result;
            }
            DEBUG_PRINT("Error: 3 compare_pair: '%s' '%s'\n", f.first.c_str(), s.first.c_str());
        }
    }
    // If exactly one value is an integer, convert the integer to a list which contains that integer as its only value, then retry the comparison. For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2); the result is then found by instead comparing [0,0,0] and [2].
    else if (is_list(first)) {
        if (second.empty()) {
            return std::make_pair(true, false);
        }

        auto result = compare_pair(first, make_list(second));
        DEBUG_PRINT("first list: %s %s %s\n", first.c_str(), second.c_str(), result.second ? "true" : "false");

        if (result.first) {
            return result;
        }
        else {
            DEBUG_PRINT("first: not done\n");
            return result;
        }
    }
    else if (is_list(second)) {
        auto result = compare_pair(make_list(first), second);
        DEBUG_PRINT("second list: %s %s %s\n", first.c_str(), second.c_str(), result.second ? "true" : "false");

        if (result.first) {
            return result;
        }
        else {
            DEBUG_PRINT("second: not done\n");
        }
    }
}

void part1(std::vector<std::string> input) {
    std::string first;
    std::string second;

    int count = 0;
    size_t i = 0;
    size_t j = 0;
    while (i < input.size()) {
        first = input[i];
        second = input[i + 1];
        i += 3;
        j += 1;

        bool done, result = false;
        std::tie(done, result) = compare_pair(first, second);
        if (result) {
            count += j;
        }
        DEBUG_PRINT("========================== %zu: %s '%s' '%s'\n", j, result ? "True" : "False", first.c_str(), second.c_str());
    }
    printf("%d\n", count);
}

// 23598 too high
void part2(std::vector<std::string> input) {
    std::string first;
    std::string second;

    std::vector<std::string> packets;
    size_t i = 0;
    while (i < input.size()) {
        if (input[i].empty()) {
            i += 1;
            continue;
        }
        packets.push_back(input[i]);
        i += 1;
    }
    packets.push_back("[[2]]");
    packets.push_back("[[6]]");
    std::sort(packets.begin(), packets.end(), [](std::string &a, std::string &b){
        return compare_pair(a, b).second;
    });

//    for (int i = 0; i < packets.size(); i++) {
//        printf("%d: %s\n", i + 1, packets[i].c_str());
//    }

    int count = 1;
    for (int i = 0; i < packets.size(); i++) {
        if (packets[i] == "[[2]]" || packets[i] == "[[6]]") {
//            printf("%d: %s\n", i, packets[i].c_str());
            count *= (i + 1);
        }
    }
    printf("%d\n", count);
}

int main() {
    std::string line;
    std::vector<std::string> input;

    while (std::getline(std::cin, line)) {
        input.push_back(line);
    }

    part1(input);
    part2(input);

    return 0;
}