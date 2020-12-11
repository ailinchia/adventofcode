package main

import (
	"bufio"
	"fmt"
	"os"
)

const (
	posFloor = '.'
	posSeatEmpty = 'L'
	posSeatOccupied = '#'
)

const maxSliceLen = 255

var maxY int
var maxX int

func occupied(seat rune) int {
	if seat == posSeatOccupied {
		return 1
	}
	return 0
}

func hasLayoutChanged(layout [maxSliceLen][maxSliceLen]rune, newLayout [maxSliceLen][maxSliceLen]rune) bool {
	for y := 0; y < maxY; y++ {
		for x := 0; x < maxX; x++ {
			if layout[y][x] != newLayout[y][x] {
				return true
			}
		}
	}

	return false
}

func getOccupiedCount(layout [maxSliceLen][maxSliceLen]rune) int {
	occupiedCount := 0
	for y := 0; y < maxY; y++ {
		for x := 0; x < maxX; x++ {
			occupiedCount += occupied(layout[y][x])
		}
	}

	return occupiedCount
}

func printLayout(layout [maxSliceLen][maxSliceLen]rune) {
	for y := 0; y < maxY; y++ {
		for x := 0; x < maxX; x++ {
			fmt.Print(string(layout[y][x]))
		}
		fmt.Print("\n")
	}
	fmt.Print("\n")
}

func seatAdjacentOccupiedCount(layout [maxSliceLen][maxSliceLen]rune, y int, x int) int {
	occupiedCount := 0
	if y > 0 {
		if x > 0 {
			occupiedCount += occupied(layout[y-1][x-1])
		}

		occupiedCount += occupied(layout[y-1][x])

		if x + 1 < maxX {
			occupiedCount += occupied(layout[y-1][x+1])
		}
	}

	if x > 0 {
		occupiedCount += occupied(layout[y][x-1])

		if y + 1 < maxY {
			occupiedCount += occupied(layout[y+1][x-1])
		}
	}

	if x + 1 < maxX {
		occupiedCount += occupied(layout[y][x+1])
	}

	if y + 1 < maxY {
		occupiedCount += occupied(layout[y+1][x])
	}

	if x < maxX && y < maxY {
		occupiedCount += occupied(layout[y+1][x+1])
	}

	return occupiedCount
}

func part1(layout [maxSliceLen][maxSliceLen]rune) {
	var newLayout[maxSliceLen][maxSliceLen] rune

	for {
		for y := 0; y < maxY; y++ {
			for x := 0; x < maxX; x++ {
				seat := layout[y][x]
				newLayout[y][x] = seat
				switch seat {
				case posSeatEmpty:
					count := seatAdjacentOccupiedCount(layout, y, x)
					if count == 0 {
						newLayout[y][x] = posSeatOccupied
					}
					break
				case posSeatOccupied:
					count := seatAdjacentOccupiedCount(layout, y, x)
					if count >= 4 {
						newLayout[y][x] = posSeatEmpty
					}
					break
				}
			}
		}

		if !hasLayoutChanged(layout, newLayout) {
			fmt.Println(getOccupiedCount(newLayout))
			return
		}

		// swap slices
		tmp := newLayout
		newLayout = layout
		layout = tmp
	}
}

func isSeat(seat rune) bool {
	return seat == posSeatEmpty || seat == posSeatOccupied
}

func seatDirectionOccupiedCount(layout[maxSliceLen][maxSliceLen] rune, y int, x int) int {
	occupiedCount := 0

	// west
	for posX := x - 1; posX >= 0; posX-- {
		seat := layout[y][posX]
		if isSeat(seat) {
			occupiedCount += occupied(seat)
			break
		}
	}

	// north west
	for posY, posX := y - 1, x - 1; posY >= 0 && posX >= 0; posY, posX = posY-1, posX-1 {
		seat := layout[posY][posX]
		if isSeat(seat) {
			occupiedCount += occupied(seat)
			break
		}
	}

	// north
	for posY := y - 1; posY >= 0; posY-- {
		seat := layout[posY][x]
		if isSeat(seat) {
			occupiedCount += occupied(seat)
			break
		}
	}

	// north east
	for posY, posX := y - 1, x + 1; posY >= 0 && posX < maxX; posY, posX = posY-1, posX+1 {
		seat := layout[posY][posX]
		if isSeat(seat) {
			occupiedCount += occupied(seat)
			break
		}
	}

	// east
	for posX := x + 1; posX < maxX; posX++ {
		seat := layout[y][posX]
		if isSeat(seat) {
			occupiedCount += occupied(seat)
			break
		}
	}

	// south east
	for posY, posX := y + 1, x + 1; posY < maxY && posX < maxX; posY, posX = posY+1, posX+1 {
		seat := layout[posY][posX]
		if isSeat(seat) {
			occupiedCount += occupied(seat)
			break
		}
	}

	// south
	for posY := y + 1; posY < maxY; posY++ {
		seat := layout[posY][x]
		if isSeat(seat) {
			occupiedCount += occupied(seat)
			break
		}
	}

	// south west
	for posY, posX := y + 1, x - 1; posY < maxY && posX >= 0; posY, posX = posY+1, posX-1 {
		seat := layout[posY][posX]
		if isSeat(seat) {
			occupiedCount += occupied(seat)
			break
		}
	}

	return occupiedCount
}

func part2(layout [maxSliceLen][maxSliceLen]rune) {
	var newLayout[maxSliceLen][maxSliceLen] rune

	for {
		for y := 0; y < maxY; y++ {
			for x := 0; x < maxX; x++ {
				seat := layout[y][x]
				newLayout[y][x] = seat
				switch seat {
				case posSeatEmpty:
					count := seatDirectionOccupiedCount(layout, y, x)
					if count == 0 && seat == posSeatEmpty {
						newLayout[y][x] = posSeatOccupied
					}
					break
				case posSeatOccupied:
					count := seatDirectionOccupiedCount(layout, y, x)
					if count >= 5 && seat == posSeatOccupied {
						newLayout[y][x] = posSeatEmpty
					}
					break
				}
			}
		}

		if !hasLayoutChanged(layout, newLayout) {
			fmt.Println(getOccupiedCount(newLayout))
			return
		}

		// swap slices
		tmp := newLayout
		newLayout = layout
		layout = tmp
	}
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var layout[maxSliceLen][maxSliceLen] rune
	y := 0
	for scanner.Scan() {
		entry := scanner.Text()
		if maxX == 0 {
			maxX = len(scanner.Text())
		}

		for x, c := range entry {
			layout[y][x] = c
		}
		y++
	}

	maxY = y

	part1(layout)
	part2(layout)
}
