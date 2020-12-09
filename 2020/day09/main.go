package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

const preambleLen = 25

func part1(entries []int, invalid *int) {
	for i := preambleLen; i < len(entries); i++ {
		valid := false
		*invalid = entries[i]
		for j := i - preambleLen; j < i + preambleLen && !valid; j++ {
			first := entries[j]
			for k := i - preambleLen; k < i + preambleLen; k++ {
				if j == k {
					continue
				}
				second := entries[k]
				if first + second == *invalid {
					valid = true
					break
				}
			}
		}

		if !valid {
			fmt.Println(*invalid)
			return
		}
	}
}

func sum(entries []int, start int, count int, max int) int {
	num := 0
	for i := start; i < start + count; i++ {
		num += entries[i]

		if num > max {
			break
		}
	}
	return num
}

func getMinMax(entries []int, start int, count int) (int, int) {
	min := entries[start]
	max := entries[start]
	for i := start + 1; i < start + count; i++ {
		num := entries[i]
		if num < min {
			min = num
		}
		if num > max {
			max = num
		}
	}
	return min, max
}

func part2(entries []int, invalid int) {
	for i := 2; i < len(entries); i++ {
		for j := 0; j < len(entries) - i; j++ {
			if sum(entries, j, i, invalid) == invalid {
				min, max := getMinMax(entries, j, i)
				fmt.Println(min + max)
				return
			}
		}
	}
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var entries []int
	for scanner.Scan() {
		if entry, err := strconv.Atoi(scanner.Text()); err == nil {
			entries = append(entries, entry)
		}
	}

	var invalid int
	part1(entries, &invalid)
	part2(entries, invalid)
}
