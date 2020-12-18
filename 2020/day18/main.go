package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func calculatePrecedenceLeftRight(expression string) int {
	exprs := strings.Split(expression, " ")
	value, _ := strconv.Atoi(exprs[0])
	for k := 1; k < len(exprs); k += 2 {
		op := exprs[k]
		num, _ := strconv.Atoi(exprs[k + 1])
		if op == "+" {
			value += num
		} else {
			value *= num
		}
	}
	return value
}

func calculateWithParenthesis(expression string, calculate func(string)int) int {
	r := []rune(expression)

	for i := len(r) - 1; i >= 0; i-- {
		var startPos int
		var endPos int

		if r[i] == '(' {
			startPos = i
			for j := i; j < len(r); j++ {
				if r[j] == ')' {
					endPos = j
					break
				}
			}

			value := calculate(string(r[startPos + 1: endPos]))
			tmp := append(r[0:startPos], []rune(strconv.Itoa(value))...)
			tmp = append(tmp, r[endPos + 1:]...)
			r = tmp
			i = len(r) - 1
		}
	}
	return calculate(string(r))
}

func part1(entries []string) {
	sum := 0
	for _, entry := range entries {
		sum += calculateWithParenthesis(entry, calculatePrecedenceLeftRight)
	}
	fmt.Println(sum)
}

func calculatePrecedencePlusMultiply(expression string) int {
	exprs := strings.Split(expression, " * ")
	var multiplies []int
	for _, expr := range exprs {
		if strings.Contains(expr, " + ") {
			v := 0
			pluses := strings.Split(expr, " + ")
			for _, plus := range pluses {
				num, _ := strconv.Atoi(plus)
				v += num
			}
			multiplies = append(multiplies, v)
		} else {
			num, _ := strconv.Atoi(expr)
			multiplies = append(multiplies, num)
		}
	}

	value := 1
	for _, multiply := range multiplies {
		value *= multiply
	}

	return value
}

func part2(entries []string) {
	sum := 0
	for _, entry := range entries {
		sum += calculateWithParenthesis(entry, calculatePrecedencePlusMultiply)
	}
	fmt.Println(sum)
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
