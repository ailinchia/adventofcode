package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

const (
	stateActive = '#'
	stateInactive = '.'
)

type dimension4d [13][13][20][20]rune


func countActiveNeighbour(d dimension4d, w int, z int, y int, x int) int {
	count := 0
	for i := int64(0); i < 81; i++ {
		s := fmt.Sprintf("%04s\n", strconv.FormatInt(i, 3))
		wN := w + int(s[0]) - '1'
		zN := z + int(s[1]) - '1'
		yN := y + int(s[2]) - '1'
		xN := x + int(s[3]) - '1'

		if wN == w && zN == z && yN == y && xN == x {
			continue
		}

		if wN > 0 && wN < 13 && zN > 0 && zN < 13 && yN > 0 && yN < 20 && xN > 0 && xN < 20 {
			if d[wN][zN][yN][xN] == stateActive {
				count += 1
			}
		}
	}

	return count
}

func runCycle(d dimension4d, minW, maxW, minZ, maxZ, minY, maxY, minX, maxX int) (dimension4d, int) {
	var newD dimension4d

	active := 0
	for w := minW; w < maxW; w++ {
		for z := minZ; z < maxZ; z++ {
			for y := minY; y < maxY; y++ {
				for x := minX; x < maxX; x++ {
					newD[w][z][y][x] = d[w][z][y][x]
					count := countActiveNeighbour(d, w, z, y, x)
					if d[w][z][y][x] == stateActive {
						if count != 2 && count != 3 {
							newD[w][z][y][x] = stateInactive
						}
					} else {
						if count == 3 {
							newD[w][z][y][x] = stateActive
						}
					}
					if newD[w][z][y][x] == stateActive {
						active++
					}
				}
			}
		}
	}
	return newD, active
}


func part1(entries []string) {
	var d dimension4d

	maxCycle := 6
	yLen := len(entries)
	xLen := len(entries[0])

	// set initial state
	for posE, entry := range entries {
		y := maxCycle + posE
		for posC, c := range entry {
			x := maxCycle + posC
			d[maxCycle][maxCycle][y][x] = c
		}
	}

	var active int
	for i := 0; i < maxCycle; i++ {
		min := maxCycle - i - 1
		max := maxCycle + i + 2
		d, active = runCycle(d, maxCycle, maxCycle + 1, min, max, min, max + yLen - 1, min, max + xLen - 1)
	}
	fmt.Println(active)
}

func part2(entries []string) {
	var d dimension4d

	maxCycle := 6
	yLen := len(entries)
	xLen := len(entries[0])

	// set initial state
	for posE, entry := range entries {
		y := maxCycle + posE
		for posC, c := range entry {
			x := maxCycle + posC
			d[maxCycle][maxCycle][y][x] = c
		}
	}

	var active int
	for i := 0; i < maxCycle; i++ {
		min := maxCycle - i - 1
		max := maxCycle + i + 2
		d, active = runCycle(d, min, max, min, max, min, max + yLen - 1, min, max + xLen - 1)
	}
	fmt.Println(active)
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var entries []string
	for scanner.Scan() {
		entries = append(entries, scanner.Text())
	}

	part1(entries)
	part2(entries)
}
