package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

var requiredFields = map[string]bool{
	"byr": true,
	"iyr": true,
	"eyr": true,
	"hgt": true,
	"hcl": true,
	"ecl": true,
	"pid": true,
}

var validECL = map[string]bool {
	"amb": true,
	"blu": true,
	"brn": true,
	"gry": true,
	"grn": true,
	"hzl": true,
	"oth": true,
}

func validPassportFieldCount(fields []string) bool {
	fieldCount := 0
	for _, field := range fields {
		pairs := strings.Split(field, ":")
		_, ok := requiredFields[pairs[0]]
		if ok {
			fieldCount += 1
		}
	}

	return fieldCount == len(requiredFields)
}

func part1(entries []string) {
	count := 0
	for _, entry := range entries {
		fields := strings.Split(entry, " ")
		if validPassportFieldCount(fields) {
			count += 1
		}
	}
	fmt.Println(count)
}

func validateInt(value string, min int64, max int64) bool {
	if valueInt, err := strconv.ParseInt(value, 10, 64); err == nil {
		if valueInt >= min && valueInt <= max {
			return true
		}
	}
	return false
}

func validPassportFields(fields []string) bool {
	for _, field := range fields {
		pairs := strings.Split(field, ":")
		key := pairs[0]
		value := pairs[1]
		_, ok := requiredFields[key]
		if ok {
			valid := false
			switch key {
			case "byr":
				if len(value) == 4 {
					valid = validateInt(value, 1920, 2002)
				}
				break
			case "iyr":
				if len(value) == 4 {
					valid = validateInt(value, 2010, 2020)
				}
				break
			case "eyr":
				if len(value) == 4 {
					valid = validateInt(value, 2020, 2030)
				}
				break
			case "hgt":
				if strings.HasSuffix(value, "cm") {
					valid = validateInt(value[:len(value) - 2], 150, 193)
				} else if strings.HasSuffix(value, "in") {
					valid = validateInt(value[:len(value) - 2], 59, 76)
				}
				break
			case "hcl":
				if value[0] == '#' && len(value) == 7 {
					if _, err := strconv.ParseInt(value[1:], 16, 64); err == nil {
						valid = true
					}
				}
				break
			case "ecl":
				_, valid = validECL[value]
				break
			case "pid":
				if len(value) == 9 {
					if _, err := strconv.ParseInt(value, 10, 64); err == nil {
						valid = true
					}
				}
				break
			}

			if !valid {
				return false
			}
		}
	}

	return true
}

func part2(entries []string) {
	count := 0
	for _, entry := range entries {
		fields := strings.Split(entry, " ")
		if validPassportFieldCount(fields) && validPassportFields(fields) {
			count += 1
		}
	}
	fmt.Println(count)
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	var entries []string
	var entry string
	for scanner.Scan() {
		line := scanner.Text()

		if len(line) > 0 {
			if len(entry) > 0 {
				entry += " "
			}
			entry += scanner.Text()
		} else {
			entries = append(entries, entry)
			entry = ""
		}
	}
	entries = append(entries, entry)

	part1(entries)
	part2(entries)
}
