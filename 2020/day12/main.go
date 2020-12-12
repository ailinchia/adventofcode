package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
)

type instruction struct {
	actions rune
	values int
}

const (
	actionMoveNorth = 'N'
	actionMoveSouth = 'S'
	actionMoveEast = 'E'
	actionMoveWest = 'W'
	actionTurnLeft = 'L'
	actionTurnRight = 'R'
	actionMoveForward = 'F'
)

const (
	directionNorth = 'N'
	directionSouth = 'S'
	directionEast = 'E'
	directionWest = 'W'
)

func move(direction rune, value int, y int, x int) (int, int) {
	switch direction {
	case directionNorth:
		y -= value
		break
	case directionEast:
		x += value
		break
	case directionSouth:
		y += value
		break
	case directionWest:
		x -= value
		break
	}
	return y, x
}

func turn(direction rune, action rune, degree int) rune {
	var turnSteps []rune
	switch action {
	case actionTurnRight:
		turnSteps = []rune{directionNorth, directionEast, directionSouth, directionWest}
		break
	case actionTurnLeft:
		turnSteps = []rune{directionNorth, directionWest, directionSouth, directionEast}
		break
	default:
		turnSteps = []rune{}
	}

	turnStep := degree / 90
	for currentStep, step := range turnSteps {
		if step == direction {
			direction = turnSteps[(currentStep + turnStep) % len(turnSteps)]
			break
		}
	}
	return direction
}

func isMoveAction(action rune) bool {
	return action == actionMoveNorth || action == actionMoveSouth || action == actionMoveEast || action == actionMoveWest || action == actionMoveForward
}

func part1(entries []instruction) {
	shipDirection := directionEast
	x := 0
	y := 0

	for _, entry := range entries {
		if isMoveAction(entry.actions) {
			direction := entry.actions
			if entry.actions == actionMoveForward {
				direction = shipDirection
			}
			y, x = move(direction, entry.values, y, x)
		} else {
			shipDirection = turn(shipDirection, entry.actions, entry.values)
		}
	}
	fmt.Println(abs(x) + abs(y))
}

const (
	waypointDirectionNorthEast = "NE"
	waypointDirectionSouthEast = "SE"
	waypointDirectionSouthWest = "SW"
	waypointDirectionNorthWest = "NW"
)

func abs(num int) int {
	return int(math.Abs(float64(num)))
}

func rotate(y int, x int, action rune, degree int) (int, int) {
	var turnSteps []string
	switch action {
	case actionTurnRight:
		turnSteps = []string{waypointDirectionNorthEast, waypointDirectionSouthEast, waypointDirectionSouthWest, waypointDirectionNorthWest}
		break
	case actionTurnLeft:
		turnSteps = []string{waypointDirectionNorthEast, waypointDirectionNorthWest, waypointDirectionSouthWest, waypointDirectionSouthEast}
		break
	default:
		turnSteps = []string{}
	}

	var direction string
	if y > 0  {
		if x > 0 {
			direction = waypointDirectionSouthEast
		} else {
			direction = waypointDirectionSouthWest
		}
	} else {
		if x > 0 {
			direction = waypointDirectionNorthEast
		} else {
			direction = waypointDirectionNorthWest
		}
	}

	turnStep := degree / 90
	for currentStep, step := range turnSteps {
		if step == direction {
			direction = turnSteps[(currentStep + turnStep) % len(turnSteps)]
			break
		}
	}

	absX := abs(x)
	absY := abs(y)

	if turnStep % 2 == 0 {
		x = absX
		y = absY
	} else {
		x = absY
		y = absX
	}

	switch direction {
	case waypointDirectionNorthEast:
		y *= -1
		break
	case waypointDirectionSouthEast:
		break
	case waypointDirectionSouthWest:
		x *= -1
		break
	case waypointDirectionNorthWest:
		y *= -1
		x *= -1
		break
	}

	return y, x
}

func part2(entries []instruction) {
	waypointX := 10
	waypointY := -1
	shipX := 0
	shipY := 0

	for _, entry := range entries {
		if isMoveAction(entry.actions) {
			if entry.actions == actionMoveForward {
				shipY += waypointY * entry.values
				shipX += waypointX * entry.values
			} else {
				waypointY, waypointX = move(entry.actions, entry.values, waypointY, waypointX)
			}
		} else {
			waypointY, waypointX = rotate(waypointY, waypointX, entry.actions, entry.values)
		}
	}
	fmt.Println(abs(shipY) + abs(shipX))
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var entries []instruction
	for scanner.Scan() {
		var entry instruction

		line := scanner.Text()
		entry.actions = rune(line[0])
		entry.values, _ = strconv.Atoi(line[1:])

		entries = append(entries, entry)
	}

	part1(entries)
	part2(entries)
}
