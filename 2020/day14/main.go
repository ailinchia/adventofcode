package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type bit struct {
	op rune
	pos int
}

type program struct {
	bitmask string
	memories []memory
}

type memory struct {
	pos       int64
	posBits   []rune
	value     int64
	valueBits []rune
}

func part1(entries []program) {
	ram := make(map[int64]int64)

	for _, entry := range entries {
		for _, mem := range entry.memories {
			var bits []bit
			for p, c := range mem.valueBits {
				if c != 'X' {
					bits = append(bits, bit{op: c, pos: p})
				}
			}
			for _, b := range bits {
				mem.valueBits[b.pos] = b.op
			}
			ram[mem.pos], _ = strconv.ParseInt(string(mem.valueBits), 2, 64)
		}
	}

	var sum int64 = 0
	for _, r := range ram {
		sum += r
	}
	fmt.Println(sum)
}

func part2(entries []program) {
	ram := make(map[int64]int64)

	for _, entry := range entries {
		xCount := strings.Count(entry.bitmask, "X")
		max, _ := strconv.ParseInt(strings.Repeat("1", xCount), 2, 64)
		for _, mem := range entry.memories {
			for p, _ := range mem.posBits {
				bitmaskBit := rune(entry.bitmask[p])
				if bitmaskBit != '0' {
					mem.posBits[p] = bitmaskBit
				}
			}

			for i := int64(0); i <= max; i++ {
				str := fmt.Sprintf(fmt.Sprintf("%%0%ds", xCount), strconv.FormatInt(i, 2))
				strPos := 0
				bits := []rune(string(mem.posBits))
				for p, c := range bits {
					if c == 'X' {
						bits[p] = rune(str[strPos])
						strPos++
					}
				}
				pos, _ := strconv.ParseInt(string(bits), 2, 64)
				ram[pos] = mem.value
			}
		}
	}

	var sum int64 = 0
	for _, r := range ram {
		sum += r
	}
	fmt.Println(sum)
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var entries []program
	var entry program

	for scanner.Scan() {
		line := scanner.Text()
		values := strings.Split(line, " = ")
		if strings.HasPrefix(values[0], "mask") {
			if len(entry.bitmask) != 0 {
				entries = append(entries, entry)
			}
			entry = program{bitmask: values[1], memories: nil}
		} else {
			var mem memory
			mem.pos, _ = strconv.ParseInt(values[0][4:len(values[0]) - 1], 10, 64)
			mem.posBits = []rune(fmt.Sprintf("%036s", strconv.FormatInt(mem.pos, 2)))
			mem.value, _ = strconv.ParseInt(values[1], 10, 64)
			mem.valueBits = []rune(fmt.Sprintf("%036s", strconv.FormatInt(mem.value, 2)))
			entry.memories = append(entry.memories, mem)
		}
	}
	entries = append(entries, entry)

	part1(entries)
	part2(entries)
}
