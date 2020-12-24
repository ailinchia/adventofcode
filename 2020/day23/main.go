package main

import (
	"bufio"
	"container/ring"
	"fmt"
	"os"
)

func printCups(cups *ring.Ring) {
	cups.Do(func(p interface{}) {
		fmt.Print(p.(int32), " ")
	})
	fmt.Println("")
}

func game(cups *ring.Ring, cupsMap map[int32]*ring.Ring, maxValue int32, maxIteration int) *ring.Ring {
	for m := 0; m < maxIteration; m++ {
		selected := cups.Unlink(3)
		selectedMap := make(map[int32]*ring.Ring)
		for i := 0; i < selected.Len(); i++ {
			selectedMap[selected.Value.(int32)] = selected
			selected = selected.Next()
		}

		found := false
		for destValue := cups.Value.(int32) - 1; !found && destValue >=  0; destValue-- {
			if _, ok := selectedMap[destValue]; ok {
				continue
			}

			if destCups, ok := cupsMap[destValue]; ok {
				destCups.Link(selected)
				found = true
				break
			}
		}
		if !found {
			for i := maxValue; i >= 0; i-- {
				if _, ok := selectedMap[i]; ok {
					continue
				}
				cupsMap[i].Link(selected)
				break
			}
		}
		cups = cups.Next()
	}

	return cups
}

func part1(cupsStr string) {
	cupsMap := make(map[int32]*ring.Ring)
	cups := ring.New(len(cupsStr))
	for _, c := range cupsStr {
		value := c - '0'
		cupsMap[value] = cups
		cups.Value = value
		cups = cups.Next()
	}

	game(cups, cupsMap, 9, 100)

	// cups after cup 1
	resultCups := cupsMap[int32(1)].Next()
	cupsMap[int32(1)].Prev().Unlink(1)
	resultCups.Do(func(p interface{}) {
		fmt.Print(p.(int32))
	})
	fmt.Println("")
}


func part2(cupsStr string) {
	cupsMap := make(map[int32]*ring.Ring)
	cups := ring.New(len(cupsStr) + 1000000 - 9)
	for _, c := range cupsStr {
		value := c - '0'
		cupsMap[value] = cups
		cups.Value = value
		cups = cups.Next()
	}
	for i := 10; i <= 1000000; i++ {
		value := int32(i)
		cupsMap[value] = cups
		cups.Value = value
		cups = cups.Next()
	}

	game(cups, cupsMap, 1000000, 10000000)

	// cups after cup 1
	firstCup := cupsMap[int32(1)].Next()
	secondCup := firstCup.Next()
	fmt.Println(int64(firstCup.Value.(int32)) * int64(secondCup.Value.(int32)))
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	if scanner.Scan() {
		line := scanner.Text()
		part1(line)
		part2(line)
	}
}
