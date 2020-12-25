package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func part1(p0 int, p1 int) {
	subjectNo := 7
	magicNo := 20201227
	value := 1
	loopSize := 1
	for  {
		value *= subjectNo
		value %= magicNo
		if value == p0 {
			break
		}
		loopSize += 1
	}
	encryptionKey := 1
	for i := 0; i < loopSize; i++ {
		encryptionKey *= p1
		encryptionKey %= magicNo
	}
	fmt.Println(encryptionKey)
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var entries []int
	for scanner.Scan() {
		line := scanner.Text()
		p, _ := strconv.Atoi(line)
		entries = append(entries, p)
	}

	if len(entries) == 2 {
		part1(entries[0], entries[1])
	}
}
