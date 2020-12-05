package main

import (
	"bufio"
	"fmt"
	"os"
)

const maxRow = 128
const maxColumn = 8

func getPos(entry string) (int, int) {
	rowCount := maxRow
	columnCount := maxColumn
	row := 0
	column := 0
	for _, c := range entry {
		switch c {
		case 'F':
			// lower half row
			rowCount /= 2
			break
		case 'B':
			// upper half row
			rowCount /= 2
			row += rowCount
			break
		case 'L':
			// lower half column
			columnCount /= 2
			break
		case 'R':
			// upper half column
			columnCount /= 2
			column += columnCount
			break
		}
	}

	return row, column
}

func getSeatID(row int, column int) int {
	return (row * 8) + column
}

func part1(entries []string) {
	maxSeatID := 0
	for _, entry := range entries {
		seatID := getSeatID(getPos(entry))
		if seatID > maxSeatID {
			maxSeatID = seatID
		}
	}
	fmt.Println(maxSeatID)
}

func part2(entries []string) {
	var plane[maxRow][maxColumn] bool
	for _, entry := range entries {
		row, column := getPos(entry)
		plane[row][column] = true
	}

	var seats []int
	for row := 0; row < maxRow; row++ {
		for column := 0; column < maxColumn; column++ {
			if !plane[row][column] {
				seats = append(seats, getSeatID(row, column))
			}
		}
	}

	for i, seat := range seats {
		if (i - 1 > 0 && seat - 1 == seats[i - 1]) || (i + 1 < len(seats) && seat + 1 == seats[i + 1]) {
			continue
		}
		fmt.Println(seat)
		break
	}
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
