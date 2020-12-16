package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type minMax struct {
	min int
	max int
}

type rule struct {
	name string
	valid []minMax
}

func isValid(field int, r rule) bool {
	for _, v := range r.valid {
		if field >= v.min && field <= v.max {
			return true
		}
	}
	return false
}

func part1(rules []rule, nearbyTickets [][]int) [][]int {
	sum := 0
	var validTickets [][]int

	for _, nearbyTicket := range nearbyTickets {
		validTicket := true
		for _, f := range nearbyTicket {
			valid := false
			for _, r := range rules {
				if isValid(f, r) {
					valid = true
					break
				}
			}

			if !valid {
				sum += f
				validTicket = false
			}
		}

		if validTicket {
			validTickets = append(validTickets, nearbyTicket)
		}
	}

	fmt.Println(sum)
	return validTickets
}

func part2(rules []rule, myTicket []int, validTickets [][]int) {
	validFieldMap := make(map[string][]int)
	fieldLen := len(validTickets[0])

	for _, r := range rules {
		for i := 0; i < fieldLen; i++ {
			valid := true
			for _, validTicket := range validTickets {
				if !isValid(validTicket[i], r) {
					valid = false
					break
				}
			}
			if valid {
				validFieldMap[r.name] = append(validFieldMap[r.name], i)
			}
		}
	}

	type field struct {
		name string
		values []int
	}

	var validFields []field
	for key, value := range validFieldMap {
		validFields = append(validFields, field{name: key, values: value})
	}
	sort.Slice(validFields, func(i, j int) bool {
		return len(validFields[i].values) < len(validFields[j].values)
	})

	sum := 1
	for i, validField := range validFields {
		if len(validField.values) == 1 {
			value := validField.values[0]

			if strings.HasPrefix(validField.name, "departure") {
				sum *= myTicket[value]
			}

			for j := i; j < len(validFields); j++ {
				otherField := validFields[j]
				for k := 0; k < len(otherField.values); k++ {
					if otherField.values[k] == value {
						otherField.values = append(otherField.values[:k], otherField.values[k+1:]...)
						break
					}
				}
				validFields[j] = otherField
			}
		}
	}
	fmt.Println(sum)
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var rules []rule
	var myTicket []int
	var nearbyTickets [][]int

	pos := 0
	for scanner.Scan() {
		line := scanner.Text()

		if len(line) == 0 {
			pos++
			continue
		}

		if pos == 0 {
			var valid1 minMax
			var valid2 minMax
			values := strings.Split(line, ":")
			n, err := fmt.Sscanf(values[1], "%d-%d or %d-%d", &valid1.min, &valid1.max, &valid2.min, &valid2.max)
			if n != 4 || err != nil {
				fmt.Println(n, err)
				return
			}

			rules = append(rules, rule{name: values[0], valid: []minMax{valid1, valid2}})
		} else if pos == 1 {
			if !strings.HasPrefix(line, "your") {
				fields := strings.Split(line, ",")
				for _, field := range fields {
					i, _ := strconv.Atoi(field)
					myTicket = append(myTicket, i)
				}
			}
		} else if pos == 2 {
			if !strings.HasPrefix(line, "nearby") {
				fields := strings.Split(line, ",")
				var nearbyTicket []int
				for _, field := range fields {
					i, _ := strconv.Atoi(field)
					nearbyTicket = append(nearbyTicket, i)
				}
				nearbyTickets = append(nearbyTickets, nearbyTicket)
			}
		}
	}

	validTickets := part1(rules, nearbyTickets)
	part2(rules, myTicket, validTickets)
}
