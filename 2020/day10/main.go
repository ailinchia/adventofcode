package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
)

func part1(entries []int) {
	diff1Count := 0
	diff3Count := 0

	for i := 0; i < len(entries)-1; i++ {
		diff := entries[i+1] - entries[i]
		if diff == 1 {
			diff1Count++
		} else if diff == 3 {
			diff3Count++
		} else if diff > 3 {
			break
		}
	}
	fmt.Println(diff1Count * diff3Count)
}

func multiplier(count int) int {
	switch count {
	case 1:
		return 2
	case 2:
		return 4
	case 3:
		return 7
	}
	return 0
}

func part2(entries []int) {
	var counts []int

	for i := 0; i < len(entries); i++ {
		count := 0
		for ; i < len(entries) - 1; {
			diff := entries[i + 1] - entries[i]
			if diff == 1 {
				count++
				i++
			} else {
				count--
				if count > 0 {
					counts = append(counts, count)
				}
				break
			}
		}
	}

	sum := 1
	for _, count := range counts {
		sum *= multiplier(count)
	}
	fmt.Println(sum)
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	entries := []int{0}
	for scanner.Scan() {
		if entry, err := strconv.Atoi(scanner.Text()); err == nil {
			entries = append(entries, entry)
		}
	}

	sort.Ints(entries)
	entries = append(entries, entries[len(entries) - 1] + 3)

	part1(entries)
	part2(entries)
}
