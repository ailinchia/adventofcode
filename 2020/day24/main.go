package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type cube struct {
	x int
	y int
	z int
}

const (
	dirNorthEast = 'd'
	dirEast = 'e'
	dirSouthEast = 'f'
	dirSouthWest = 'g'
	dirWest = 'w'
	dirNorthWest = 'c'
)

func moveCube(direction rune) cube {
	switch direction {
	case dirNorthWest:
		return cube{0, 1, -1}
	case dirNorthEast:
		return cube{1, 0, -1}
	case dirEast:
		return cube{1, -1, 0}
	case dirSouthEast:
		return cube{0, -1, 1}
	case dirSouthWest:
		return cube{-1, 0, 1}
	case dirWest:
		return cube{-1, 1, 0}
	}
	return cube{0, 0, 0}
}

func countBlack(floor map[cube]bool) int {
	count := 0
	for _, v := range floor {
		if v {
			count++
		}
	}
	return count
}

func part1(entries []string) map[cube]bool {
	floor := make(map[cube]bool)
	for _, entry := range entries {
		var c cube
		entry = strings.ReplaceAll(entry, "ne", string(dirNorthEast))
		entry = strings.ReplaceAll(entry, "nw", string(dirNorthWest))
		entry = strings.ReplaceAll(entry, "se", string(dirSouthEast))
		entry = strings.ReplaceAll(entry, "sw", string(dirSouthWest))
		for _, e := range entry {
			mc := moveCube(e)
			c.x += mc.x
			c.y += mc.y
			c.z += mc.z
		}
		floor[c] = !floor[c]
	}

	fmt.Println(countBlack(floor))

	return floor
}

func addCorner(floor map[cube]bool, corners map[cube]bool, c cube, direction rune) {
	m := moveCube(direction)
	c.x += m.x
	c.y += m.y
	c.z += m.z

	if _, ok := floor[c]; !ok {
		floor[c] = false
		corners[c] = false
	}
}

func addCorners(floor map[cube]bool, corners map[cube]bool) map[cube]bool {
	if len(corners) == 0 {
		corners = floor
	}

	newCorners := make(map[cube]bool)
	for c, _ := range corners {
		addCorner(floor, newCorners, c, dirNorthWest)
		addCorner(floor, newCorners, c, dirNorthEast)
		addCorner(floor, newCorners, c, dirEast)
		addCorner(floor, newCorners, c, dirSouthEast)
		addCorner(floor, newCorners, c, dirSouthWest)
		addCorner(floor, newCorners, c, dirWest)
	}
	return newCorners
}

func isBlack(floor map[cube]bool, c cube, direction rune) bool {
	m := moveCube(direction)
	c.x += m.x
	c.y += m.y
	c.z += m.z
	return floor[c]
}

func part2(floor map[cube]bool) {
	corners := make(map[cube]bool)
	for d := 0; d < 100; d++ {
		corners = addCorners(floor, corners)
		newFloor := make(map[cube]bool)
		for c, v := range floor {
			blackCount := 0
			if isBlack(floor, c, dirNorthWest) {
				blackCount++
			}
			if isBlack(floor, c, dirNorthEast) {
				blackCount++
			}
			if isBlack(floor, c, dirEast) {
				blackCount++
			}
			if isBlack(floor, c, dirSouthEast) {
				blackCount++
			}
			if isBlack(floor, c, dirSouthWest) {
				blackCount++
			}
			if isBlack(floor, c, dirWest) {
				blackCount++
			}

			newFloor[c] = v
			if v {
				if blackCount == 0 || blackCount > 2 {
					newFloor[c] = false
				}
			} else {
				if blackCount == 2 {
					newFloor[c] = true
				}
			}
		}
		floor = newFloor
	}

	fmt.Println(countBlack(floor))
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var entries []string
	for scanner.Scan() {
		entries = append(entries, scanner.Text())
	}

	floor := part1(entries)
	part2(floor)
}
