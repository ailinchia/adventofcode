package main

import (
	"bufio"
	"fmt"
	"os"
)

type Entry struct {
	minCount int
	maxCount int
	letter byte
	password string
}

func validatePart1Entry(entry Entry) bool {
	count := 0
	for _, c := range entry.password {
		if c == rune(entry.letter) {
			count += 1
		}
	}
	return count >= entry.minCount && count <= entry.maxCount
}

func part1(entries []Entry) {
	count := 0
	for _, entry := range entries {
		if validatePart1Entry(entry) {
			count += 1
		}
	}
	fmt.Println(count)
}

func validatePart2Entry(entry Entry) bool {
	return (entry.letter == entry.password[entry.minCount - 1]) != (entry.letter == entry.password[entry.maxCount - 1])
}

func part2(entries []Entry) {
	count := 0
	for _, entry := range entries {
		if validatePart2Entry(entry) {
			count += 1
		}
	}
	fmt.Println(count)
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var entries []Entry

	for scanner.Scan() {
		var entry Entry
		c, err := fmt.Sscanf(scanner.Text(), "%d-%d %c: %s", &entry.minCount, &entry.maxCount, &entry.letter, &entry.password)
		if c != 4 || err != nil {
			fmt.Printf("error parsing input='%v' count=%v err=%v", scanner.Text(), c, err)
			os.Exit(1)
		}

		entries = append(entries, entry)
	}

	part1(entries)
	part2(entries)
}
