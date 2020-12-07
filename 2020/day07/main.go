package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func getOuterBags(innerOuterBag map[string][]string, bagColors []string, outerBag map[string]bool) {
	for _, bagColor := range bagColors {
		outerBag[bagColor] = true
		outerBagColors, ok := innerOuterBag[bagColor]
		if ok {
			getOuterBags(innerOuterBag, outerBagColors, outerBag)
		}
	}
}

func part1(entries []string) {
	innerOuterBag := make(map[string][]string)
	for _, entry := range entries {
		values := strings.Split(entry, " contain ")
		words := strings.Split(values[0], " ")
		outerBagColor := fmt.Sprintf("%s %s", words[0], words[1])

		bagContains := strings.Split(values[1], ", ")
		for _, bag := range bagContains {
			words := strings.Split(bag, " ")
			if _, err := strconv.Atoi(words[0]); err == nil {
				insideBagColor := fmt.Sprintf("%s %s", words[1], words[2])
				innerOuterBag[insideBagColor] = append(innerOuterBag[insideBagColor], outerBagColor)
			}
		}
	}

	outerBag := make(map[string]bool)
	getOuterBags(innerOuterBag, []string{"shiny gold"}, outerBag)
	fmt.Println(len(outerBag) - 1)
}

type bagPair struct {
	color string
	count int
}

func getInnerBagCount(outerInnerBag map[string][]bagPair, bagPairs []bagPair) int {
	count := 0
	for _, bagPair := range bagPairs {
		var bagCount int
		innerBag, ok := outerInnerBag[bagPair.color]
		if ok {
			bagCount = (bagPair.count * getInnerBagCount(outerInnerBag, innerBag)) + bagPair.count
		} else {
			bagCount = bagPair.count
		}

		count += bagCount
	}
	return count
}

func part2(entries []string) {
	outerInnerBag := make(map[string][]bagPair)
	for _, entry := range entries {
		values := strings.Split(entry, " contain ")
		words := strings.Split(values[0], " ")
		outerBagColor := fmt.Sprintf("%s %s", words[0], words[1])

		bagContains := strings.Split(values[1], ", ")
		for _, bag := range bagContains {
			words := strings.Split(bag, " ")
			if _, err := strconv.Atoi(words[0]); err == nil {
				var insideBagColor string
				insideBagCount, err := strconv.Atoi(words[0])
				if err != nil {
					insideBagCount = 1
				} else {
					insideBagColor = fmt.Sprintf("%s %s", words[1], words[2])
				}
				outerInnerBag[outerBagColor] = append(outerInnerBag[outerBagColor], bagPair{
					color: insideBagColor,
					count: insideBagCount,
				})
			}
		}
	}

	fmt.Println(getInnerBagCount(outerInnerBag, []bagPair{{"shiny gold", 1}}) - 1)
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
