#include <string>
#include <iostream>
#include <algorithm>
#include <bitset>

std::string extractBitString(const std::string &input, unsigned &i) {
    auto n = 8;
    if (i + n >= input.size()) {
        n = input.size() - i;
//        std::cout << "n=" << n << " i=" << i << " size=" << input.size() << std::endl;
    }

    auto currentStr = std::string(input.c_str(), i, n);
    i += n;

    std::bitset<32> bits(std::stoul(currentStr, nullptr, 16));
    auto bitStr = bits.to_string();
    if (n < 8) {
        bitStr.erase(0, (8 - n) * 4);
    }
    return bitStr;
}

std::string extractBits(const std::string &input, unsigned &i, std::string &currentBitString, unsigned numBits, unsigned &packetBitsLength) {
    if (currentBitString.size() < numBits) {
        currentBitString += extractBitString(input, i);
    }

    auto bitStr = currentBitString.substr(0, numBits);
    currentBitString.erase(0, numBits);
    packetBitsLength += numBits;

    return bitStr;
}

std::pair<unsigned, uint64_t> processPacket(const std::string &input, unsigned &i, std::string &currentBitString, unsigned &totalVersion) {
    unsigned packetBitsLength = 0;
    uint64_t value = 0;

    auto versionStr = extractBits(input, i, currentBitString, 3, packetBitsLength);
    auto version = std::stoi(versionStr, nullptr, 2);
    totalVersion += version;

    auto id = std::stoi(extractBits(input, i, currentBitString, 3, packetBitsLength), nullptr, 2);
    if (id == 4) {
        // literal value
        bool done = false;
        do {
            auto bitString = extractBits(input, i, currentBitString, 5, packetBitsLength);
            if (bitString.front() == '0') {
                done = true;
            }
            bitString.erase(0, 1);

            value |= std::stoi(bitString, nullptr, 2);
            if (!done) {
                value <<= 4;
            }

        } while (!done);
    } else {
        // operator
        std::vector<uint64_t> values;
        auto lengthTypeId = extractBits(input, i, currentBitString, 1, packetBitsLength);
        if (lengthTypeId == "0") {
            // next 15 bits total length of subpackets in bits
            auto bitStr = extractBits(input, i, currentBitString, 15, packetBitsLength);
            auto subPacketSize = std::stoul(bitStr, nullptr, 2);
            unsigned processedSubPacketSize = 0;
            while (processedSubPacketSize < subPacketSize) {
                auto result = processPacket(input, i, currentBitString, totalVersion);
                processedSubPacketSize += result.first;
                packetBitsLength += result.first;
                values.push_back(result.second);
            }
        } else if (lengthTypeId == "1") {
            // next 11 bits number of sub-packets
            auto numberSubPacket = std::stoi(extractBits(input, i, currentBitString, 11, packetBitsLength), nullptr, 2);
            for (int j = 0; j < numberSubPacket; j++) {
                auto result = processPacket(input, i, currentBitString, totalVersion);
                packetBitsLength += result.first;
                values.push_back(result.second);
            }
        }

        if (id == 0) {
            // sum
            for (auto v : values) {
                value += v;
            }
        } else if (id == 1) {
            value = 1;
            // product
            for (auto v : values) {
                value *= v;
            }
        } else if (id == 2) {
            value = UINT64_MAX;
            // min
            for (auto v : values) {
                value = std::min(value, v);
            }
        } else if (id == 3) {
            // max
            for (auto v : values) {
                value = std::max(value, v);
            }
        } else if (id == 5) {
            // greater than
            value = (values[0] > values[1]) ? 1 : 0;
        } else if (id == 6) {
            // less than
            value = (values[0] < values[1]) ? 1 : 0;
        } else if (id == 7) {
            // equals to
            value = (values[0] == values[1]) ? 1 : 0;
        }
    }
    return std::make_pair(packetBitsLength, value);
}

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) {
        exit(1);
    }

    std::string currentBitString;
    unsigned totalVersion = 0;
    unsigned i = 0;

    auto result = processPacket(line, i, currentBitString, totalVersion);

    // part1
    std::cout << totalVersion << std::endl;

    // part2
    std::cout << result.second << std::endl;

    return 0;
}