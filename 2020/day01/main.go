package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func part1(entries []int64) {
	for x, entryX := range entries {
		for y, entryY := range entries {
			if x == y {
				continue
			}

			if entryX + entryY == 2020 {
				fmt.Println(entryX * entryY)
				return
			}
		}
	}
}

func part2(entries []int64) {
	for x, entryX := range entries {
		for y, entryY := range entries {
			for z, entryZ := range entries {
				if x == y || y == z || z == x {
					continue
				}

				if entryX + entryY + entryZ == 2020 {
					fmt.Println(entryX * entryY * entryZ)
					return
				}
			}
		}
	}
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var entries []int64
	for scanner.Scan() {
		entry, err := strconv.ParseInt(scanner.Text(), 10, 64)
		if err != nil {
			fmt.Printf("error parsing input=%v err=%v", scanner.Text(), err)
			os.Exit(1)
		}

		entries = append(entries, entry)
	}

	part1(entries)
	part2(entries)
}
