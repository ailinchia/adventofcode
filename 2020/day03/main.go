package main

import (
	"bufio"
	"fmt"
	"os"
)

func countTrees(entries []string, right int, down int) int {
	x := 0
	count := 0
	for y, entry := range entries {
		if y == 0 || y % down != 0 {
			continue
		}

		x += right
		if x >= len(entry) {
			x %= len(entry)
		}

		if entry[x] == '#' {
			count += 1
		}
	}

	return count
}

func part1(entries []string) {
	fmt.Println(countTrees(entries, 3, 1))
}

func part2(entries []string) {
	fmt.Println(countTrees(entries, 1, 1) *
		countTrees(entries, 3, 1) *
		countTrees(entries, 5, 1) *
		countTrees(entries, 7, 1) *
		countTrees(entries, 1, 2))
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
