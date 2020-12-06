package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func part1(entries []string) {
	count := 0
	for _, entry := range entries {
		unique := make(map[rune]bool)
		for _, c := range entry {
			if c == ' ' {
				continue
			}
			_, ok := unique[c]
			if !ok {
				unique[c] = true
				count += 1
			}
		}
	}
	fmt.Println(count)
}

func part2(entries []string) {
	count := 0
	for _, entry := range entries {
		answers := make(map[rune]int)
		persons := strings.Split(entry, " ")
		for _, person := range persons {
			for _, c := range person {
				answers[c] += 1
			}
		}
		for _, value := range answers {
			if value == len(persons) {
				count += 1
			}
		}
	}
	fmt.Println(count)
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var entries []string
	var entry string
	for scanner.Scan() {
		line := scanner.Text()

		if len(line) > 0 {
			if len(entry) > 0 {
				entry += " "
			}
			entry += scanner.Text()
		} else {
			entries = append(entries, entry)
			entry = ""
		}
	}
	entries = append(entries, entry)

	part1(entries)
	part2(entries)
}
