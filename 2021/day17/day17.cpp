#include <string>
#include <iostream>
#include <algorithm>

bool hitTarget(int x, int y, int targetMinX, int targetMinY, int targetMaxX, int targetMaxY) {
    return (x >= targetMinX && x <= targetMaxX && y >= targetMinY && y <= targetMaxY);
}

bool outOfBounds(int x, int y, int targetMaxX, int targetMinY, int velocityX) {
    return ((x > targetMaxX || velocityX == 0) && y < targetMinY);
}

int main() {
    // target area: x=20..30, y=-10..-5
    int targetMinX = 0, targetMinY = 0, targetMaxX = 0, targetMaxY = 0;
    std::string tmpStr;
    std::cin.ignore(256, '=');
    if (std::cin >> tmpStr) {
        size_t idx = 0;
        targetMinX = std::stoi(tmpStr, &idx);
        targetMaxX = std::stoi(tmpStr.substr(idx + 2));
    }
    std::cin.ignore(256, '=');
    if (std::cin >> tmpStr) {
        size_t idx = 0;
        targetMinY = std::stoi(tmpStr, &idx);
        targetMaxY = std::stoi(tmpStr.substr(idx + 2));
    }

    int maxY = INT32_MIN;
    int count = 0;
    for (int vx = -200; vx <= 200; vx++) {
        for (int vy = -200; vy <= 200; vy++) {
            int cvx = vx;
            int cvy = vy;
            int x = 0, y = 0;

            int currentMaxY = INT32_MIN;
            while (!outOfBounds(x, y, targetMaxX, targetMinY, cvx)) {
                x += cvx;
                y += cvy;

                currentMaxY = std::max(y, currentMaxY);
                if (hitTarget(x, y, targetMinX, targetMinY, targetMaxX, targetMaxY)) {
                    maxY = std::max(maxY, currentMaxY);
                    count++;
                    break;
                }

                if (cvx > 0) {
                    cvx -= 1;
                } else if (cvx < 0) {
                    cvx += 1;
                }

                cvy -= 1;
            }
        }
    }
    std::cout << maxY << std::endl;
    std::cout << count << std::endl;

    return 0;
}