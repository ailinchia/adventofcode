package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func expandRule(rules map[int]string, ruleNo int, max int) string {
	rule := rules[ruleNo]
	for i := 0; i < max && strings.ContainsAny(rule, "0123456789"); i++ {
		newRule := ""
		for _, r := range strings.Split(rule, " ") {
			n, err := strconv.Atoi(r)
			if err != nil {
				newRule += r + " "
				continue
			}
			value := rules[n]
			if value == "a" || value == "b" {
				newRule += fmt.Sprintf("%s ", value)
			} else {
				newRule += fmt.Sprintf("( %s ) ", value)
			}
		}
		rules[ruleNo] = newRule
		rule = newRule
	}

	return "^" + strings.Join(strings.Fields(rules[ruleNo]), "") + "$"
}

func part1(rules map[int]string, messages []string) {
	regexStr := expandRule(rules, 0, 100)
	r, _ := regexp.Compile(regexStr)
	matches := 0
	for _, m := range messages {
		if r.MatchString(m) {
			matches++
		}
	}
	fmt.Println(matches)
}

func part2(rules map[int]string, messages []string) {
	// 8: 42 | 42 8
	// 11: 42 31 | 42 11 31
	rules[8] = "( 42 )+"
	rules[11] = "42 31 | 42 11 31"

	regexStr := expandRule(rules, 0, 15)
	r, _ := regexp.Compile(regexStr)
	matches := 0
	for _, m := range messages {
		if r.MatchString(m) {
			matches++
		}
	}
	fmt.Println(matches)
}

func copyMap(m map[int]string) map[int]string {
	newMap := make(map[int]string)
	for k, v := range m {
		newMap[k] = v
	}
	return newMap
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	rules := make(map[int]string)
	var messages []string

	pos := 0
	for scanner.Scan() {
		line := scanner.Text()
		if len(line) == 0 {
			pos++
			continue
		}

		if pos == 0 {
			// 0: 4 1 5
			// 1: 2 3 | 3 2
			// 4: "a"
			values := strings.Split(line, ": ")
			pos, _ := strconv.Atoi(values[0])
			value := strings.Trim(values[1], "\"")
			rules[pos] = value
		} else {
			// ababbb
			// bababa
			messages = append(messages, line)
		}
	}

	part1(copyMap(rules), messages)
	part2(copyMap(rules), messages)
}
