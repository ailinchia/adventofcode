package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func calculateScore(p1 []int, p2 []int) int {
	p := &p1
	if len(p2) != 0 {
		p = &p2
	}

	score := 0
	for i, n := range *p {
		score += n * (len(*p) - i)
	}
	return score
}
func part1(p1 []int, p2 []int) {
	for ; len(p1) > 0 && len(p2) > 0; {
		if p1[0] > p2[0] {
			p1 = append(p1[1:], p1[0], p2[0])
			p2 = p2[1:]
		} else {
			p2 = append(p2[1:], p2[0], p1[0])
			p1 = p1[1:]
		}
	}

	fmt.Println(calculateScore(p1, p2))
}

type round struct {
	p1 []int
	p2 []int
}

func equal(a []int, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i, v := range a {
		if v != b[i] {
			return false
		}
	}
	return true
}

func checkRound(rounds []round, p1 []int, p2 []int) (bool, []round) {
	newP1 := append([]int{}, p1...)
	newP2 := append([]int{}, p2...)
	p1 = newP1
	p2 = newP2

	for _, r := range rounds {
		if equal(r.p1, p1) && equal(r.p2, p2) {
			return true, rounds
		}
	}

	return false, append(rounds, round{p1, p2})
}

func game(p1 []int, p2 []int) ([]int, []int) {
	var rounds []round

	newP1 := append([]int{}, p1...)
	newP2 := append([]int{}, p2...)
	p1 = newP1
	p2 = newP2

	for ; len(p1) > 0 && len(p2) > 0; {
		var found bool
		found, rounds = checkRound(rounds, p1, p2)
		if found {
			return p1, []int{}
		}

		if p1[0] < len(p1) && p2[0] < len(p2) {
			// sub game
			_, sp2 := game(p1[1:p1[0] + 1], p2[1:p2[0] + 1])
			if len(sp2) == 0 {
				p1 = append(p1[1:], p1[0], p2[0])
				p2 = p2[1:]
			} else {
				p2 = append(p2[1:], p2[0], p1[0])
				p1 = p1[1:]
			}
		} else {
			// main game
			if p1[0] > p2[0] {
				p1 = append(p1[1:], p1[0], p2[0])
				p2 = p2[1:]
			} else {
				p2 = append(p2[1:], p2[0], p1[0])
				p1 = p1[1:]
			}
		}
	}

	return p1, p2
}

func part2(p1 []int, p2 []int) {
	fmt.Println(calculateScore(game(p1, p2)))
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var p1 []int
	var p2 []int

	p := &p1
	for scanner.Scan() {
		line := scanner.Text()
		if len(line) == 0 {
			p = &p2
			continue
		}

		if strings.HasPrefix(line, "Player") {
			continue
		}

		n, _ := strconv.Atoi(line)
		*p = append(*p, n)
	}

	part1(p1, p2)
	part2(p1, p2)
}
