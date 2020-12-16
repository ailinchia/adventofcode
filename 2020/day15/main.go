package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func getSpokenNumber(entries []int, at int) int {
	entryMap := make(map[int][]int)
	for i, entry := range entries {
		entryMap[entry] = append(entryMap[entry], i + 1)
	}

	lastNumber := entries[len(entries) - 1]
	startTurn := len(entries) + 1
	for turn := startTurn; turn <= at; turn++ {
		if len(entryMap[lastNumber]) - 1 == 0 {
			lastNumber = 0
			entryMap[lastNumber] = append(entryMap[lastNumber], turn)
		} else {
			values := entryMap[lastNumber]
			lastNumber = values[len(values) - 1] - values[len(values) - 2]
			entryMap[lastNumber] = append(entryMap[lastNumber], turn)
		}
	}
	return lastNumber
}

func part1(entries []int) {
	fmt.Println(getSpokenNumber(entries, 2020))
}

func part2(entries []int) {
	fmt.Println(getSpokenNumber(entries, 30000000))
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var entries []int
	for scanner.Scan() {
		values := strings.Split(scanner.Text(), ",")
		for _, value := range values {
			n, _ := strconv.Atoi(value)
			entries = append(entries, n)
		}
	}

	part1(entries)
	part2(entries)
}
